from abc import ABCMeta, abstractmethod

from domain.mails.entities import Mail


class CoordinatorGateway(metaclass=ABCMeta):
    """Абстрактный шлюз для координации обработки почтовых сообщений.

    Определяет интерфейс для управления процессом отправки или обработки
    списка почтовых сообщений.
    """

    @abstractmethod
    async def run(self, mails: list[Mail]): ...

    """Запускает обработку переданного списка почтовых сообщений."""
