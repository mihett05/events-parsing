from application.transactions import Transaction, TransactionsGateway
from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction


class DatabaseTransaction(Transaction):
    """
    Реализация интерфейса Transaction для работы с транзакциями SQLAlchemy.

    Обеспечивает базовые операции commit и rollback для управления транзакциями.
    """

    def __init__(self, transaction: AsyncSessionTransaction):
        self.__transaction = transaction

    async def commit(self):
        """Фиксирует текущую транзакцию в базе данных."""

        await self.__transaction.commit()

    async def rollback(self):
        """Откатывает текущую транзакцию."""

        await self.__transaction.rollback()


class TransactionsDatabaseGateway(TransactionsGateway):
    """
    Шлюз для управления транзакциями в базе данных.

    Поддерживает вложенные транзакции и автоматическое управление
    жизненным циклом транзакций через контекстный менеджер.
    """

    __transaction: AsyncSessionTransaction | None = None

    def __init__(
        self,
        session: AsyncSession,
        transaction: AsyncSessionTransaction | None = None,
    ):
        self.__session = session
        self.__transaction = transaction

    async def __aenter__(self) -> Transaction:
        self.__transaction = self.__session.begin_nested()
        await self.__transaction.__aenter__()
        return DatabaseTransaction(self.__transaction)

    def nested(self) -> "TransactionsDatabaseGateway":
        """Создает новый шлюз для вложенной транзакции."""

        return TransactionsDatabaseGateway(
            self.__session, self.__session.begin_nested()
        )

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Обрабатывает завершение транзакции при выходе из контекста."""

        if self.__transaction and self.__transaction.is_active:
            if exc_type is None:
                await self.__transaction.commit()
            else:
                await self.__transaction.rollback()

        if self.__transaction:
            await self.__transaction.__aexit__(exc_type, exc_val, exc_tb)
        if self.__session.in_nested_transaction():
            self.__transaction = self.__session.get_nested_transaction()
        else:
            self.__transaction = None
