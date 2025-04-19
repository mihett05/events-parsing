from abc import ABCMeta, abstractmethod

from domain.mails.entities import Mail


class EmailsGateway(metaclass=ABCMeta):

    @abstractmethod
    async def receive_mails(self) -> list[Mail]: ...
