from abc import ABCMeta, abstractmethod

from domain.mails.dtos import ParsedMailInfoDto


class EmailsGateway(metaclass=ABCMeta):
    @abstractmethod
    async def receive_mails(self) -> list[ParsedMailInfoDto]: ...

    @abstractmethod
    async def mark_mails_as_failed(self, mail_ids: list[str]): ...
