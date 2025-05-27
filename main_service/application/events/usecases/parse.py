import asyncio

from domain.mails.dtos import ReadAllMailsDto
from domain.mails.entities import Mail

from application.attachments.gateways import FilesGateway
from application.mails.usecases import ReadUnprocessedMailUseCase

from ..coordinator.gateway import CoordinatorGateway


class ParseEventsUseCase:
    """Кейс использования для парсинга событий из входящих писем.
    Осуществляет обработку непрочитанных писем, извлечение вложений
    и передачу данных в координатор для дальнейшей обработки.
    """

    def __init__(
        self,
        coordinator_gateway: CoordinatorGateway,
        mail_read_unprocessed_use_case: ReadUnprocessedMailUseCase,
        files_gateway: FilesGateway,
    ):
        """Инициализирует зависимости"""

        self.__coordinator_gateway = coordinator_gateway
        self.__mail_read_unprocessed_use_case = mail_read_unprocessed_use_case
        self.__files_gateway = files_gateway

    async def __call__(self):
        """Основной метод обработки писем.
        Читает письма пачками, добавляет ссылки к вложениям
        и передает письма в координатор для обработки.
        Обработка происходит порционно через пагинацию.
        """

        dto = ReadAllMailsDto(page=0, page_size=50)
        while mails := await self.__mail_read_unprocessed_use_case(dto):
            await self.__add_links(mails)
            await self.__coordinator_gateway.run(mails)
            dto.page += 1

    async def __add_links(self, mails: list[Mail]):
        """Добавляет ссылки к вложениям писем.

        Для каждого вложения каждого письма асинхронно
        запрашивает и добавляет ссылку через файловый шлюз.
        """

        await asyncio.gather(
            *[
                self.__files_gateway.add_link_to_attachment(attachment)
                for mail in mails
                for attachment in mail.attachments
            ]
        )
