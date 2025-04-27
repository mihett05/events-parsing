import shutil
from typing import Iterable

import pytest_asyncio
from dishka import AsyncContainer
from fastapi import FastAPI
from fastapi.testclient import TestClient

from infrastructure.api.app import create_app
from infrastructure.config import Config, get_config
from infrastructure.providers.container import create_container


@pytest_asyncio.fixture(scope="package")
async def container() -> Iterable[AsyncContainer]:
    container = create_container()
    yield container
    await container.close()


@pytest_asyncio.fixture(scope="package")
async def config() -> Config:
    return get_config()


@pytest_asyncio.fixture(scope="package", autouse=True)
async def get_app(container: AsyncContainer, config: Config):
    app = create_app(container, config)
    yield app
    shutil.rmtree("static")


@pytest_asyncio.fixture(scope="package", autouse=True)
async def get_test_client(get_app: FastAPI) -> TestClient:
    yield TestClient(get_app)