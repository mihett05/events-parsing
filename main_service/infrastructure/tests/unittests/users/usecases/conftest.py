import application.auth.usecases as auth_usecases
import application.users.usecases as user_usecases
import pytest_asyncio
from dishka import AsyncContainer


@pytest_asyncio.fixture
async def register_user_usecase(
    container: AsyncContainer,
) -> auth_usecases.RegisterUseCase:
    async with container() as nested:
        yield await nested.get(auth_usecases.RegisterUseCase)


@pytest_asyncio.fixture
async def create_user_usecase(
    container: AsyncContainer,
) -> user_usecases.CreateUserUseCase:
    async with container() as nested:
        yield await nested.get(user_usecases.CreateUserUseCase)


@pytest_asyncio.fixture
async def read_user_usecase(
    container: AsyncContainer,
) -> user_usecases.ReadUserUseCase:
    async with container() as nested:
        yield await nested.get(user_usecases.ReadUserUseCase)


@pytest_asyncio.fixture
async def update_user_usecase(
    container: AsyncContainer,
) -> user_usecases.UpdateUserUseCase:
    async with container() as nested:
        yield await nested.get(user_usecases.UpdateUserUseCase)


@pytest_asyncio.fixture
async def delete_user_usecase(
    container: AsyncContainer,
) -> user_usecases.DeleteUserUseCase:
    async with container() as nested:
        yield await nested.get(user_usecases.DeleteUserUseCase)


@pytest_asyncio.fixture
async def read_all_users_usecase(
    container: AsyncContainer,
) -> user_usecases.ReadAllUsersUseCase:
    async with container() as nested:
        yield await nested.get(user_usecases.ReadAllUsersUseCase)
