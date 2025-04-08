from contextvars import ContextVar, Token

from application.transactions import Transaction, TransactionsGateway
from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

transaction_var: ContextVar[AsyncSessionTransaction | None] = ContextVar(
    "transaction_var", default=None
)


class DatabaseTransaction(Transaction):
    def __init__(self, transaction: AsyncSessionTransaction):
        self.__transaction = transaction

    async def commit(self):
        await self.__transaction.commit()

    async def rollback(self):
        await self.__transaction.rollback()


class TransactionsDatabaseGateway(TransactionsGateway):
    __token: Token | None = None
    __transaction: AsyncSessionTransaction | None = None

    def __init__(
        self,
        session: AsyncSession,
        transaction: AsyncSessionTransaction | None = None,
    ):
        self.__token = None
        self.__session = session
        self.__transaction = transaction

    async def __aenter__(self) -> Transaction:
        if not self.__transaction:
            self.__transaction = self.__session.begin()
        await self.__transaction.__aenter__()
        self.__token = transaction_var.set(self.__transaction)
        return DatabaseTransaction(self.__transaction)

    def nested(self) -> "TransactionsDatabaseGateway":
        return TransactionsDatabaseGateway(
            self.__session, self.__session.begin_nested()
        )

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.__token:
            transaction_var.reset(self.__token)
        if self.__transaction:
            await self.__transaction.__aexit__(exc_type, exc_val, exc_tb)
        self.__transaction = None
