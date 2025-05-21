import shutil
from typing import Iterable

import pytest_asyncio
from dishka import AsyncContainer
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from infrastructure.api.app import create_app
from infrastructure.config import Config, get_config
from infrastructure.mocks.providers.container import (
    create_integration_test_container,
)


@pytest_asyncio.fixture
async def container() -> Iterable[AsyncContainer]:
    container = create_integration_test_container()
    yield container
    await container.close()


@pytest_asyncio.fixture
async def config() -> Config:
    return get_config()


@pytest_asyncio.fixture
async def get_app(container: AsyncContainer, config: Config):
    app = create_app(container, config)
    yield app
    shutil.rmtree("static")


@pytest_asyncio.fixture(autouse=True)
async def get_test_client(get_app: FastAPI) -> AsyncClient:
    transport = ASGITransport(app=get_app)
    async with AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        yield client
