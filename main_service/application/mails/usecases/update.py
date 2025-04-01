from application.mails.dtos import UpdateMailDto
from application.mails.usecases.read import ReadMailUseCase
from application.transactions import TransactionsGateway
from domain.mails.entities import Mail

from domain.mails.repositories import MailsRepository


class UpdateMailUseCase:
    def __init__(
        self,
        repository: MailsRepository,
        read_use_case: ReadMailUseCase,
        tx: TransactionsGateway,
    ):
        self.__repository = repository
        self.__transaction = tx
        self.__read_use_case = read_use_case

    async def __call__(self, dto: UpdateMailDto) -> Mail:
        async with self.__transaction:
            mail = await self.__read_use_case(dto.id)

            mail.event_id = dto.event_id
            mail.state = dto.state

            return await self.__repository.update(mail)
