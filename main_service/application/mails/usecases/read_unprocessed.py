from domain.mails.dtos import ReadAllMailsDto
from domain.mails.entities import Mail
from domain.mails.repositories import MailsRepository


class ReadUnprocessedMailUseCase:
    def __init__(self, repository: MailsRepository):
        self.__repository = repository

    async def __call__(self, dto: ReadAllMailsDto) -> list[Mail]:
        return await self.__repository.read_unprocessed(dto)
