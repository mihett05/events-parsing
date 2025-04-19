from abc import ABCMeta, abstractmethod

import domain.mails.dtos as dtos
import domain.mails.entities as entities


class MailsRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create(self, dto: dtos.CreateMailDto) -> entities.Mail: ...

    @abstractmethod
    async def read(self, mail_id: int) -> entities.Mail: ...

    @abstractmethod
    async def read_unprocessed(
        self, dto: dtos.ReadAllMailsDto
    ) -> list[entities.Mail]: ...

    @abstractmethod
    async def update(self, event: entities.Mail) -> entities.Mail: ...

    @abstractmethod
    async def create_many(self, dtos: list[dtos.CreateMailDto]) -> list[entities.Mail]: ...
