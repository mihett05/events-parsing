from abc import ABCMeta, abstractmethod

from domain.attachments.entities import Attachment


class FilesGateway(metaclass=ABCMeta):
    @abstractmethod
    async def read(self, attachment: Attachment) -> Attachment: ...

    @abstractmethod
    async def create(self, attachment: Attachment) -> Attachment: ...

    @abstractmethod
    async def delete(self, attachment: Attachment) -> Attachment: ...
