from datetime import datetime, timedelta
from typing import Any, Callable, Coroutine
from uuid import UUID

import pytest
import pytest_asyncio
from application.auth.dtos import AuthenticateUserDto, RegisterUserDTO
from application.auth.tokens.dtos import TokenInfoDto
from application.auth.tokens.gateways import TokensGateway
from application.auth.usecases import RegisterUseCase
from dishka import AsyncContainer
from domain.users.entities import User, UserActivationToken
from domain.users.repositories import UsersRepository


@pytest_asyncio.fixture
async def register_user1_dto() -> RegisterUserDTO:
    return RegisterUserDTO(
        email="test@example.com",
        password="12345678",
        fullname="Ivanov Ivan Ivanovich",
    )


@pytest_asyncio.fixture
async def user_1_activation_token() -> UserActivationToken:
    return UserActivationToken(
        user_id=1,
        user=User(
            email="test@test.com",
            fullname="Ivanov Ivan Ivanovich",
        ),
        id=UUID(int=1),
    )


@pytest_asyncio.fixture
async def authenticate_user1_dto() -> AuthenticateUserDto:
    return AuthenticateUserDto(
        email="test@example.com",
        password="12345678",
    )


@pytest_asyncio.fixture
async def user1_token_info_dto() -> TokenInfoDto:
    date = datetime.now().date()
    return TokenInfoDto(
        subject="test@example.com",
        expires_in=datetime.combine(date, datetime.min.time())
        + timedelta(days=1),
    )


@pytest_asyncio.fixture
async def authenticate_user1_broken_password_dto() -> AuthenticateUserDto:
    return AuthenticateUserDto(email="test@example.com", password="1_23_56_8")


@pytest_asyncio.fixture
async def register_user2_dto() -> RegisterUserDTO:
    return RegisterUserDTO(
        email="tset@tset.moc",
        password="87654321",
        fullname="Romanov Roman Romanovich",
    )


@pytest_asyncio.fixture
async def user_2_activation_token() -> UserActivationToken:
    return UserActivationToken(
        user_id=2,
        user=User(
            email="tset@tset.moc",
            fullname="Romanov Roman Romanovich",
        ),
        id=UUID(int=2),
    )


@pytest_asyncio.fixture
async def authenticate_user2_dto() -> AuthenticateUserDto:
    return AuthenticateUserDto(email="tset@tset.moc", password="87654321")


@pytest_asyncio.fixture
async def user2_token_info_dto() -> TokenInfoDto:
    date = datetime.now().date()
    return TokenInfoDto(
        subject="tset@tset.moc",
        expires_in=datetime.combine(date, datetime.min.time())
        + timedelta(days=1),
    )



@pytest_asyncio.fixture
async def token_gateway(container: AsyncContainer) -> TokensGateway:
    async with container() as nested:
        yield await nested.get(TokensGateway)


@pytest_asyncio.fixture
async def users_repository(container: AsyncContainer) -> UsersRepository:
    async with container() as nested:
        yield await nested.get(UsersRepository)


@pytest_asyncio.fixture
async def create_user1(
    register_user1_dto: RegisterUserDTO,
    register_usecase: RegisterUseCase,
    users_repository: UsersRepository,
) -> Callable[..., Coroutine[Any, Any, User]]:
    async def _factory() -> User:
        token1 = await register_usecase(register_user1_dto)
        return token1.user

    return _factory


@pytest_asyncio.fixture
async def create_user2(
    register_user2_dto: RegisterUserDTO,
    register_usecase: RegisterUseCase,
    users_repository: UsersRepository,
) -> User:
    token2 = await register_usecase(register_user2_dto)
    return token2.user


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare(
    pytestconfig: pytest.Config, users_repository: UsersRepository
):
    if pytestconfig.getoption("--integration", default=False):
        return
    await users_repository.clear()  # noqa


@pytest_asyncio.fixture(scope="function", autouse=True)
async def teardown(
    pytestconfig: pytest.Config, users_repository: UsersRepository
):
    yield
    if pytestconfig.getoption("--integration", default=False):
        return
    await users_repository.clear()  # noqa
