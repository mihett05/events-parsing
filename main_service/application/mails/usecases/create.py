from domain.mails.dtos import CreateMailDto
from domain.mails.entities import Mail

from domain.mails.repositories import MailsRepository


class CreateMailUseCase:
    def __init__(self, repository: MailsRepository):
        self.__repository = repository

    async def __call__(self, dto: CreateMailDto) -> Mail:
        return await self.__repository.create(dto)
