from abc import ABCMeta, abstractmethod

from domain.mails.entities import Mail


class CoordinatorGateway(metaclass=ABCMeta):
    @abstractmethod
    async def run(self, mails: list[Mail]): ...
