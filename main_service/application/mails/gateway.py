from abc import ABCMeta, abstractmethod

from domain.mails.dtos import ParsedMailInfoDto


class EmailsGateway(metaclass=ABCMeta):
    """
    Абстрактный шлюз для работы с электронной почтой.

    Определяет интерфейс для получения и обработки писем из внешней почтовой системы.
    Реализации должны обеспечивать взаимодействие с конкретными почтовыми сервисами.
    """

    @abstractmethod
    async def receive_mails(self) -> list[ParsedMailInfoDto]: ...

    """
    Получает и парсит новые письма из почтовой системы.
    """

    @abstractmethod
    async def mark_mails_as_failed(self, mail_ids: list[str]): ...

    """
    Помечает указанные письма как ошибочно обработанные.
    """
