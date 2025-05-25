import asyncio
from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from infrastructure.config import Config
from infrastructure.database.postgres import get_engine, get_session_maker
from infrastructure.database.transactions import (
    TransactionsDatabaseGateway,
    TransactionsGateway,
)


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_engine(self, config: Config) -> AsyncEngine:
        return get_engine(str(config.postgres_url))

    @provide(scope=Scope.APP)
    def get_session_maker(self, engine: AsyncEngine) -> async_sessionmaker:
        return get_session_maker(engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker(expire_on_commit=False) as session:
            yield session
            await session.commit()
        await asyncio.shield(session.close())

    @provide(scope=Scope.REQUEST)
    async def get_transaction(self, session: AsyncSession) -> TransactionsGateway:
        return TransactionsDatabaseGateway(session)
