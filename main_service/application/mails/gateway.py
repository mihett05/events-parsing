from abc import ABCMeta, abstractmethod

from domain.mails.dtos import ParsedMailInfoDto


class EmailsGateway(metaclass=ABCMeta):

    @abstractmethod
    async def receive_mails(self) -> list[ParsedMailInfoDto]: ...
