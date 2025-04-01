from domain.mails.entities import Mail

from domain.mails.repositories import MailsRepository


class ReadMailUseCase:
    def __init__(self, repository: MailsRepository):
        self.__repository = repository

    async def __call__(self, mail_id: int) -> Mail:
        return await self.__repository.read(mail_id)
