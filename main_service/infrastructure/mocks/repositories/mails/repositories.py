from datetime import datetime

from domain.mails import dtos as dtos
from domain.mails import entities as entities
from domain.mails.dtos import CreateMailDto
from domain.mails.entities import Mail
from domain.mails.enums import MailStateEnum
from domain.mails.exceptions import (
    MailAlreadyExistsError,
    MailNotFoundError,
)
from domain.mails.repositories import MailsRepository

from ..crud import Id, MockRepository, MockRepositoryConfig
from .mappers import map_create_dto_to_entity


class MailsMemoryRepository(MailsRepository):
    class Config(MockRepositoryConfig):
        def __init__(self):
            super().__init__(
                entity=Mail,
                not_found_exception=MailNotFoundError,
                already_exists_exception=MailAlreadyExistsError,
            )

        def extract_id(self, entity: Mail) -> Id:
            return entity.id

    def __init__(self):
        self.__next_id = 1
        self.__repository = MockRepository(self.Config())

    async def create_many(
        self, create_dtos: list[dtos.CreateMailDto]
    ) -> list[entities.Mail]:
        return [await self.create(dto) for dto in create_dtos]

    async def create(self, dto: CreateMailDto) -> Mail:
        mail = map_create_dto_to_entity(dto)

        mail.id = self.__next_id
        self.__next_id += 1

        return await self.__repository.create(mail)

    async def read(self, mail_id: int) -> Mail:
        return await self.__repository.read(mail_id)

    async def read_unprocessed(
        self, dto: dtos.ReadAllMailsDto
    ) -> list[entities.Mail]:
        data = await self.__repository.read_all()
        return [
            mail
            for mail in data
            if mail.state == MailStateEnum.UNPROCESSED
            and mail.retry_after >= datetime.utcnow()
        ]

    async def update(self, mail: Mail) -> Mail:
        return await self.__repository.update(mail)

    async def delete(self, mail: Mail) -> Mail:
        return await self.__repository.delete(mail)
