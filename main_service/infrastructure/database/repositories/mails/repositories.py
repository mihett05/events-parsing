import domain.mails.dtos as dtos
from domain.mails.entities import Mail
from domain.mails.enums import MailStateEnum
from domain.mails.exceptions import MailAlreadyExists, MailNotFound
from domain.mails.repositories import MailsRepository
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import LoaderOption

from ..repository import Id, PostgresRepository, PostgresRepositoryConfig
from .mappers import map_create_dto_to_model, map_from_db, map_to_db
from .models import MailDatabaseModel


class MailsDatabaseRepository(MailsRepository):
    class Config(PostgresRepositoryConfig):
        def __init__(self):
            super().__init__(
                model=MailDatabaseModel,
                entity=Mail,
                entity_mapper=map_from_db,
                model_mapper=map_to_db,
                create_model_mapper=map_create_dto_to_model,
                not_found_exception=MailNotFound,
                already_exists_exception=MailAlreadyExists,
            )

        def extract_id_from_entity(self, entity: Mail) -> Id:
            return entity.id

        def extract_id_from_model(self, model: MailDatabaseModel) -> Id:
            return model.id

        def get_options(self) -> list[LoaderOption]:
            return []

        def get_select_all_query(self, dto: dtos.ReadAllMailsDto) -> Select:
            return (
                select(self.model)
                .filter_by(state=MailStateEnum.UNPROCESSED)
                .order_by(self.model.id.desc())
                .offset(dto.page * dto.page_size)
                .limit(dto.page_size)
            )

    def __init__(self, session: AsyncSession):
        self.__session = session
        self.__repository = PostgresRepository(session, self.Config())

    async def read_unprocessed(self, dto: dtos.ReadAllMailsDto) -> list[Mail]:
        return await self.__repository.read_all(dto)

    async def create(self, dto: dtos.CreateMailDto) -> Mail:
        return await self.__repository.create(dto)

    async def read(self, mail_id: int) -> Mail:
        return await self.__repository.read(mail_id)

    async def update(self, mail: Mail) -> Mail:
        return await self.__repository.update(mail)
