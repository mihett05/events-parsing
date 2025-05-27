from domain.mails.dtos import ReadAllMailsDto
from domain.mails.entities import Mail
from domain.mails.repositories import MailsRepository


class ReadUnprocessedMailUseCase:
    """
    Сценарий чтения непрочитанных почтовых сообщений.

    Обеспечивает получение списка писем, которые еще не были обработаны,
    в соответствии с заданными критериями выборки.
    """

    def __init__(self, repository: MailsRepository):
        """
        Инициализирует сценарий с использованием репозитория для работы с почтой.
        """

        self.__repository = repository

    async def __call__(self, dto: ReadAllMailsDto) -> list[Mail]:
        """
        Выполняет сценарий чтения непрочитанных писем.

        Возвращает:
            Список почтовых сообщений, соответствующих критериям выборки.
        """

        return await self.__repository.read_unprocessed(dto)
