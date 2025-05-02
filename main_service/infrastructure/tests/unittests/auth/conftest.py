from datetime import datetime, timedelta

import pytest_asyncio
from application.auth.dtos import AuthenticateUserDto, RegisterUserDTO
from application.auth.tokens.dtos import TokenInfoDto
from application.auth.tokens.gateways import TokensGateway
from application.auth.usecases import RegisterUseCase
from dishka import AsyncContainer
from domain.users.entities import User
from domain.users.repositories import UsersRepository


@pytest_asyncio.fixture
async def register_user1_dto() -> RegisterUserDTO:
    return RegisterUserDTO(
        email="test@test.com",
        password="12345678",
        fullname="Ivanov Ivan Ivanovich",
    )


@pytest_asyncio.fixture
async def authenticate_user1_dto() -> AuthenticateUserDto:
    return AuthenticateUserDto(
        email="test@test.com",
        password="12345678",
    )


@pytest_asyncio.fixture
async def user1_token_info_dto() -> TokenInfoDto:
    date = datetime.now().date()
    return TokenInfoDto(
        subject="test@test.com",
        expires_in=datetime.combine(date, datetime.min.time()) + timedelta(days=1),
    )


@pytest_asyncio.fixture
async def authenticate_user1_broken_password_dto() -> AuthenticateUserDto:
    return AuthenticateUserDto(email="test@test.com", password="1_345_7_")


@pytest_asyncio.fixture
async def register_user2_dto() -> RegisterUserDTO:
    return RegisterUserDTO(
        email="tset@tset.moc",
        password="87654321",
        fullname="Romanov Roman Romanovich",
    )


@pytest_asyncio.fixture
async def authenticate_user2_dto() -> AuthenticateUserDto:
    return AuthenticateUserDto(email="tset@tset.moc", password="87654321")


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
) -> User:
    user1, _ = await register_usecase(register_user1_dto)
    return user1


@pytest_asyncio.fixture
async def create_user2(
    register_user2_dto: RegisterUserDTO,
    register_usecase: RegisterUseCase,
    users_repository: UsersRepository,
) -> User:
    user2, _ = await register_usecase(register_user2_dto)
    return user2
