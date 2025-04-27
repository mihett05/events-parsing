from application.mails.usecases import ReadUnprocessedMailUseCase
from domain.mails.dtos import ReadAllMailsDto

from ..coordinator.gateway import CoordinatorGateway


class ParseEventsUseCase:
    def __init__(
        self,
        coordinator_gateway: CoordinatorGateway,
        mail_read_unprocessed_use_case: ReadUnprocessedMailUseCase,
    ):
        self.__coordinator_gateway = coordinator_gateway
        self.__mail_read_unprocessed_use_case = mail_read_unprocessed_use_case

    async def __call__(self):
        dto = ReadAllMailsDto(page=0, page_size=50)

        while mails := await self.__mail_read_unprocessed_use_case(dto):
            await self.__coordinator_gateway.run(mails)
            dto.page += 1
