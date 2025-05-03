import pytest
import pytest_asyncio

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
