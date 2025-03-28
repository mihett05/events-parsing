import pytest_asyncio


@pytest_asyncio.fixture
async def container():
    container = ...
    yield container
    await container.close()
