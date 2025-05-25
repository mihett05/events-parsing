from datetime import datetime, timedelta
from typing import Any, Callable, Coroutine
from uuid import UUID

import pytest
import pytest_asyncio
from application.auth.dtos import AuthenticateUserDto, RegisterUserDto
from application.auth.tokens.dtos import TokenInfoDto
from application.auth.tokens.gateways import TokensGateway
from application.auth.usecases import RegisterUseCase
from dishka import AsyncContainer
from domain.users.entities import User, UserActivationToken
from domain.users.repositories import UsersRepository

from infrastructure.config import Config


@pytest_asyncio.fixture
async def register_user_dto(container: AsyncContainer) -> RegisterUserDto:
    config = await container.get(Config)
    return RegisterUserDto(
        email=config.imap_username,
        password="12345678",
        fullname="Ivanov Ivan Ivanovich",
    )


@pytest_asyncio.fixture
async def get_user_authenticate_dto() -> AuthenticateUserDto:
    return AuthenticateUserDto(email="public@public.com", password="public")


@pytest_asyncio.fixture
async def get_user_authorize_token_info_dto() -> TokenInfoDto:
    date = datetime.now().date()
    return TokenInfoDto(
        subject="public@public.com",
        expires_in=datetime.combine(date, datetime.min.time()) + timedelta(days=1),
    )


@pytest_asyncio.fixture
async def authenticate_user1_broken_password_dto() -> AuthenticateUserDto:
    return AuthenticateUserDto(email="test@gmail.com", password="1_23_56_8")


@pytest_asyncio.fixture
async def token_gateway(container: AsyncContainer) -> TokensGateway:
    async with container() as nested:
        yield await nested.get(TokensGateway)


@pytest_asyncio.fixture
async def users_repository(container: AsyncContainer) -> UsersRepository:
    async with container() as nested:
        yield await nested.get(UsersRepository)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare(pytestconfig: pytest.Config, users_repository: UsersRepository):
    if pytestconfig.getoption("--integration", default=False):
        return
    await users_repository.clear()  # noqa


@pytest_asyncio.fixture(scope="function", autouse=True)
async def teardown(pytestconfig: pytest.Config, users_repository: UsersRepository):
    yield
    if pytestconfig.getoption("--integration", default=False):
        return
    await users_repository.clear()  # noqa
