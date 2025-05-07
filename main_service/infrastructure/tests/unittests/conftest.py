import pytest
import pytest_asyncio
from dishka import AsyncContainer
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from domain.users.entities import User
from infrastructure.database.postgres import Base
from infrastructure.tests.configs import get_container


def pytest_addoption(parser):
    parser.addoption(
        "--integration",
        action="store_true",
        help="Run tests with testcontainers",
    )


@pytest_asyncio.fixture(scope="session")
async def container(pytestconfig: pytest.Config):
    async with get_container(
        bool(pytestconfig.getoption("--integration", default=False))
    ) as container:
        try:
            yield container
        finally:
            await container.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db_tables(
    pytestconfig: pytest.Config, container: AsyncContainer
):
    if not pytestconfig.getoption("--integration", default=False):
        return
    engine = await container.get(AsyncEngine)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_data(pytestconfig: pytest.Config, container: AsyncContainer):
    if not pytestconfig.getoption("--integration", default=False):
        return
    engine = await container.get(AsyncEngine)
    async with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(
                text(f"TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE")
            )


@pytest_asyncio.fixture
async def get_user_entity() -> User:
    return User(
        email="test@example.com",
        fullname="Ivanov Ivan Ivanovich",
    )


@pytest_asyncio.fixture
async def get_user_entities() -> list[User]:
    return [
        User(
            email=f"test{i}@test.com",
            fullname=f"Ivan{i}",
        )
        for i in range(8)
    ]


