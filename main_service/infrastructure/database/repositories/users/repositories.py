from uuid import UUID

import domain.users.dtos as dtos
from application.auth.dtos import CreateUserWithPasswordDto
from domain.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from domain.users import entities as entities
from domain.users.entities import (
    PasswordResetToken,
    TelegramToken,
    User,
    UserActivationToken,
    UserOrganizationRole,
)
from domain.users.exceptions import (
    TelegramTokenAlreadyExistsError,
    TelegramTokenNotFoundError,
    UserAlreadyExistsError,
    UserNotFoundError,
    UserRoleAlreadyExistsError,
    UserRoleNotFoundError,
)
from domain.users.repositories import (
    TelegramTokensRepository,
    UserActivationTokenRepository,
    UserOrganizationRolesRepository,
    UsersRepository,
)
from sqlalchemy import Select, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.interfaces import LoaderOption

from infrastructure.config import Config

from ..repository import PostgresRepository, PostgresRepositoryConfig
from .mappers import (
    create_password_reset_token_map,
    create_user_activation_token_map,
    create_user_mapper,
    map_from_db,
    map_to_db,
    password_reset_token_map_from_db,
    password_reset_token_map_to_db,
    telegram_token_map_create_to_model,
    telegram_token_map_from_db,
    telegram_token_map_to_db,
    user_activation_token_map_from_db,
    user_activation_token_map_to_db,
    user_organization_role_map_from_db,
    user_organization_role_map_to_db,
)
from .models import (
    PasswordResetTokenDatabaseModel,
    TelegramTokenDatabaseModel,
    UserActivationTokenDatabaseModel,
    UserDatabaseModel,
    UserOrganizationRoleDatabaseModel,
    UserSettingsDatabaseModel,
)


class UsersDatabaseRepository(UsersRepository):
    """Репозиторий для работы с пользователями в базе данных."""

    class RepositoryConfig(PostgresRepositoryConfig):
        """Конфигурация репозитория пользователей."""

        def __init__(self):
            """Инициализирует конфигурацию маппинга пользователей."""

            super().__init__(
                model=UserDatabaseModel,
                entity=User,
                entity_mapper=map_from_db,
                model_mapper=map_to_db,
                create_model_mapper=create_user_mapper,
                not_found_exception=UserNotFoundError,
                already_exists_exception=UserAlreadyExistsError,
            )

        def get_select_by_email_query(self, email: str) -> Select:
            """Формирует запрос для поиска пользователя по email."""

            return select(self.model).where(self.model.email == email)

        def get_select_all_query(self, dto: dtos.ReadAllUsersDto) -> Select:
            """Формирует запрос для постраничного чтения пользователей."""

            return (
                select(self.model)
                .order_by(self.model.id)
                .offset(dto.page * dto.page_size)
                .limit(dto.page_size)
            )

        def get_options(self) -> list[LoaderOption]:
            """Возвращает опции для загрузки связанных сущностей."""

            return [selectinload(self.model.settings)]

        def get_select_by_calendar_uuid(self, uuid: UUID) -> Select:
            """Формирует запрос для поиска пользователя по UUID календаря."""

            return (
                select(self.model)
                .join(self.model.settings)
                .where(UserSettingsDatabaseModel.calendar_uuid == uuid)
            )

    def __init__(self, session: AsyncSession, config: Config):
        """Инициализирует репозиторий пользователей."""

        self.__config = self.RepositoryConfig()
        self.__session = session
        self.__repository = PostgresRepository(session, self.__config)
        self.__const = config

    async def read_all(self, dto: dtos.ReadAllUsersDto) -> list[entities.User]:
        """Возвращает список пользователей с пагинацией."""

        return await self.__repository.read_all(dto)

    async def read_by_ids(self, user_ids: list[int]) -> list[entities.User]:
        """Возвращает пользователей по списку идентификаторов."""

        return await self.__repository.read_by_ids(user_ids)

    async def create(self, dto: CreateUserWithPasswordDto) -> User:
        """Создает нового пользователя с паролем."""

        model: UserDatabaseModel = self.__config.create_model_mapper(dto)
        model.settings = UserSettingsDatabaseModel()
        return await self.__repository.create(model)

    async def read(self, user_id: int) -> User:
        """Возвращает пользователя по идентификатору."""

        return await self.__repository.read(user_id)

    async def read_by_email(self, email: str) -> entities.User:
        """Возвращает пользователя по email."""

        if model := await self.__repository.get_scalar_or_none(
            self.__config.get_select_by_email_query(email)
        ):
            return self.__config.model_mapper(model)
        raise self.__config.not_found_exception

    async def read_by_calendar_uuid(self, uuid: UUID) -> entities.User:
        """Возвращает пользователя по UUID связанного календаря."""

        if model := await self.__repository.get_scalar_or_none(
            self.__config.get_select_by_calendar_uuid(uuid)
        ):
            return self.__config.model_mapper(model)
        raise self.__config.not_found_exception

    async def get_super_user(self) -> User:
        """Возвращает суперпользователя системы."""

        return await self.read_by_email(self.__const.admin_username)

    async def update(self, user: User) -> User:
        """Обновляет данные пользователя."""

        return await self.__repository.update(user)

    async def delete(self, user: entities.User) -> entities.User:
        """Удаляет пользователя."""

        return await self.__repository.delete(user)

    async def change_user_active_status(self, user_id: int, status: bool):
        """Изменяет статус активности пользователя."""

        query = (
            update(UserDatabaseModel)
            .where(UserDatabaseModel.id == user_id)
            .values(is_active=status)
            .execution_options(synchronize_session="fetch")
            .returning(self.__config.model)
        )
        await self.__session.execute(query)


class UserOrganizationRolesDatabaseRepository(UserOrganizationRolesRepository):
    """Репозиторий для работы с ролями пользователей в организациях."""

    class Config(PostgresRepositoryConfig):
        """Конфигурация репозитория ролей пользователей в организациях."""

        def __init__(self):
            """Инициализирует конфигурацию маппинга ролей."""

            super().__init__(
                model=UserOrganizationRoleDatabaseModel,
                entity=UserOrganizationRole,
                entity_mapper=user_organization_role_map_from_db,
                model_mapper=user_organization_role_map_to_db,
                create_model_mapper=None,
                not_found_exception=UserRoleNotFoundError,
                already_exists_exception=UserRoleAlreadyExistsError,
            )

        def get_select_all_query(self, user_id: int) -> Select:
            """Формирует запрос для получения всех ролей пользователя."""

            return select(self.model).where(self.model.user_id == user_id)

        def extract_id_from_entity(self, entity: UserOrganizationRole):
            """Извлекает идентификаторы из сущности роли."""

            return {
                "organization_id": entity.organization_id,
                "user_id": entity.user_id,
            }

        def extract_id_from_model(self, model: UserOrganizationRoleDatabaseModel):
            """Извлекает идентификаторы из модели роли."""

            return {
                "organization_id": model.organization_id,
                "user_id": model.user_id,
            }

    def __init__(self, session: AsyncSession):
        """Инициализирует репозиторий ролей пользователей."""

        self.__config = self.Config()
        self.__session = session
        self.__repository = PostgresRepository(session, self.__config)

    async def create(self, role: UserOrganizationRole) -> UserOrganizationRole:
        """Создает новую роль пользователя в организации."""

        # TODO: сделать идемпотентным
        return await self.__repository.create_from_entity(role)

    async def read(self, user_id: int, organization_id: int) -> UserOrganizationRole:
        """Возвращает роль пользователя в конкретной организации."""

        return await self.__repository.read(
            {"user_id": user_id, "organization_id": organization_id}
        )

    async def read_all(self, user_id: int) -> list[UserOrganizationRole]:
        """Возвращает все роли пользователя в организациях."""

        return await self.__repository.read_all(user_id)

    async def update(self, role: UserOrganizationRole) -> UserOrganizationRole:
        """Обновляет данные роли пользователя в организации."""

        return await self.__repository.update(role)

    async def delete(self, role: UserOrganizationRole) -> UserOrganizationRole:
        """Удаляет роль пользователя в организации."""

        return await self.__repository.delete(role)


class TelegramTokensDatabaseRepository(TelegramTokensRepository):
    """Репозиторий для работы с Telegram токенами пользователей."""

    class Config(PostgresRepositoryConfig):
        """Конфигурация репозитория Telegram токенов."""

        def __init__(self):
            """Инициализирует конфигурацию маппинга Telegram токенов."""

            super().__init__(
                model=TelegramTokenDatabaseModel,
                entity=TelegramToken,
                entity_mapper=telegram_token_map_from_db,
                model_mapper=telegram_token_map_to_db,
                create_model_mapper=telegram_token_map_create_to_model,
                not_found_exception=TelegramTokenNotFoundError,
                already_exists_exception=TelegramTokenAlreadyExistsError,
            )

    def __init__(self, session: AsyncSession):
        """Инициализирует репозиторий Telegram токенов."""

        self.__session = session
        self.__config = self.Config()
        self.__repository = PostgresRepository(session, self.__config)

    async def create(self, dto: dtos.CreateTelegramTokenDto) -> TelegramToken:
        """Создает новый Telegram токен для пользователя."""

        return await self.__repository.create_from_dto(dto)

    async def read(self, token_id: UUID) -> TelegramToken:
        """Возвращает Telegram токен по идентификатору."""

        return await self.__repository.read(token_id)

    async def update(self, token: TelegramToken) -> TelegramToken:
        """Обновляет данные Telegram токена."""

        return await self.__repository.update(token)


class UserActivationTokenDatabaseRepository(UserActivationTokenRepository):
    """Репозиторий для работы с токенами активации пользователей."""

    class Config(PostgresRepositoryConfig):
        """Конфигурация репозитория токенов активации."""

        def __init__(self):
            """Инициализирует конфигурацию маппинга токенов активации."""

            super().__init__(
                model=UserActivationTokenDatabaseModel,
                entity=UserActivationToken,
                entity_mapper=user_activation_token_map_from_db,
                model_mapper=user_activation_token_map_to_db,
                create_model_mapper=create_user_activation_token_map,
                not_found_exception=EntityNotFoundError,
                already_exists_exception=EntityAlreadyExistsError,
            )

        def get_options(self) -> list[LoaderOption]:
            """Возвращает опции для загрузки связанных сущностей."""

            return [
                selectinload(self.model.user).selectinload(UserDatabaseModel.settings)
            ]

    def __init__(self, session: AsyncSession):
        """Инициализирует репозиторий токенов активации."""

        self.__config = self.Config()
        self.__session = session
        self.__repository = PostgresRepository(session, self.__config)

    async def create(self, dto: dtos.CreateActivationTokenDto) -> UserActivationToken:
        """Создает новый токен активации пользователя."""

        # TODO: remove this shit
        query = (
            insert(self.__config.model)
            .values(id=dto.id, user_id=dto.user_id)
            .returning(self.__config.model)
        )
        result = await self.__session.scalars(self.__config.add_options(query))
        model = result.one()
        return self.__config.entity_mapper(model)

    async def read(self, token_id: UUID) -> UserActivationToken:
        """Возвращает токен активации по идентификатору."""

        return await self.__repository.read(token_id)

    async def change_token_used_statement(self, token_id: UUID):
        """Помечает токен активации как использованный."""

        query = (
            update(UserActivationTokenDatabaseModel)
            .where(UserActivationTokenDatabaseModel.id == token_id)
            .values(is_used=True)
            .execution_options(synchronize_session="fetch")
            .returning(self.__config.model)
        )
        await self.__session.execute(query)

    async def delete(self, token: UserActivationToken) -> UserActivationToken:
        """Удаляет токен активации."""

        return await self.__repository.delete(token)


class PasswordResetTokenDatabaseRepository(UserActivationTokenRepository):
    class Config(PostgresRepositoryConfig):
        def __init__(self):
            super().__init__(
                model=PasswordResetTokenDatabaseModel,
                entity=PasswordResetToken,
                entity_mapper=password_reset_token_map_from_db,
                model_mapper=password_reset_token_map_to_db,
                create_model_mapper=create_password_reset_token_map,
                not_found_exception=EntityNotFoundError,
                already_exists_exception=EntityAlreadyExistsError,
            )

        def get_options(self) -> list[LoaderOption]:
            return [
                selectinload(self.model.user).selectinload(UserDatabaseModel.settings)
            ]

    def __init__(self, session: AsyncSession):
        self.__config = self.Config()
        self.__session = session
        self.__repository = PostgresRepository(session, self.__config)

    async def create(self, dto: dtos.CreatePasswordResetTokenDto) -> PasswordResetToken:
        return await self.__repository.create_from_dto(dto)

    async def read(self, token_id: UUID) -> PasswordResetToken:
        return await self.__repository.read(token_id)

    async def change_token_used_statement(self, token_id: UUID):
        query = (
            update(PasswordResetTokenDatabaseModel)
            .where(PasswordResetTokenDatabaseModel.id == token_id)
            .values(is_used=True)
            .execution_options(synchronize_session="fetch")
            .returning(self.__config.model)
        )
        await self.__session.execute(query)

    async def delete(self, token: PasswordResetToken) -> PasswordResetToken:
        return await self.__repository.delete(token)
