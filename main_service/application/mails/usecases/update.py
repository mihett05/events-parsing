from domain.mails.entities import Mail
from domain.mails.repositories import MailsRepository

from application.mails.dtos import UpdateMailDto
from application.mails.usecases.read import ReadMailUseCase
from application.transactions import TransactionsGateway


class UpdateMailUseCase:
    """
    Сценарий обновления данных почтового сообщения.

    Обеспечивает атомарное изменение состояния письма и его привязки к событию,
    гарантируя целостность данных в рамках транзакции.
    """

    def __init__(
        self,
        repository: MailsRepository,
        read_use_case: ReadMailUseCase,
        tx: TransactionsGateway,
    ):
        """
        Инициализирует сценарий с зависимостями для работы с хранилищем,
        чтением сообщений и управлением транзакциями.
        """

        self.__repository = repository
        self.__transaction = tx
        self.__read_use_case = read_use_case

    async def __call__(self, dto: UpdateMailDto) -> Mail:
        """
        Выполняет обновление данных почтового сообщения.

        Возвращает:
            Обновленный экземпляр почтового сообщения с новым состоянием
            и привязкой к событию.
        """

        async with self.__transaction:
            mail = await self.__read_use_case(dto.id)

            mail.event_id = dto.event_id
            mail.state = dto.state

            return await self.__repository.update(mail)
