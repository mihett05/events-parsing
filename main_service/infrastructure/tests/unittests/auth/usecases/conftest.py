import application.auth.usecases as auth_usecases
import pytest_asyncio
from dishka import AsyncContainer


@pytest_asyncio.fixture
async def register_usecase(
    container: AsyncContainer,
) -> auth_usecases.RegisterUseCase:
    async with container() as nested:
        yield await nested.get(auth_usecases.RegisterUseCase)


@pytest_asyncio.fixture
async def authenticate_usecase(
    container: AsyncContainer,
) -> auth_usecases.AuthenticateUseCase:
    async with container() as nested:
        yield await nested.get(auth_usecases.AuthenticateUseCase)


@pytest_asyncio.fixture
async def authorize_usecase(
    container: AsyncContainer,
) -> auth_usecases.AuthorizeUseCase:
    async with container() as nested:
        yield await nested.get(auth_usecases.AuthorizeUseCase)


@pytest_asyncio.fixture
async def create_token_pair_usecase(
    container: AsyncContainer,
) -> auth_usecases.CreateTokenPairUseCase:
    async with container() as nested:
        yield await nested.get(auth_usecases.CreateTokenPairUseCase)


@pytest_asyncio.fixture
async def login_usecase(
    container: AsyncContainer,
) -> auth_usecases.LoginUseCase:
    async with container() as nested:
        yield await nested.get(auth_usecases.LoginUseCase)
