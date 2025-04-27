import pytest_asyncio

from infrastructure.mocks.providers.container import create_unittest_container


@pytest_asyncio.fixture
async def container():
    container = create_unittest_container()
    yield container
    await container.close()
