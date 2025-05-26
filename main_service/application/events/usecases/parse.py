import asyncio

from domain.mails.dtos import ReadAllMailsDto
from domain.mails.entities import Mail

from application.attachments.gateways import FilesGateway
from application.mails.usecases import ReadUnprocessedMailUseCase

from ..coordinator.gateway import CoordinatorGateway


class ParseEventsUseCase:
    def __init__(
        self,
        coordinator_gateway: CoordinatorGateway,
        mail_read_unprocessed_use_case: ReadUnprocessedMailUseCase,
        files_gateway: FilesGateway,
    ):
        self.__coordinator_gateway = coordinator_gateway
        self.__mail_read_unprocessed_use_case = mail_read_unprocessed_use_case
        self.__files_gateway = files_gateway

    async def __call__(self):
        dto = ReadAllMailsDto(page=0, page_size=50)
        while mails := await self.__mail_read_unprocessed_use_case(dto):
            await self.__add_links(mails)
            await self.__coordinator_gateway.run(mails)
            dto.page += 1

    async def __add_links(self, mails: list[Mail]):
        await asyncio.gather(
            *[
                self.__files_gateway.add_link_to_attachment(attachment)
                for mail in mails
                for attachment in mail.attachments
            ]
        )
