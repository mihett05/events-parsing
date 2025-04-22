from abc import ABCMeta, abstractmethod

from domain.attachments.entities import Attachment

from application.attachments.dtos import CreateAttachmentDto


class FilesGateway(metaclass=ABCMeta):
    @abstractmethod
    async def read(self, path: str) -> Attachment: ...

    @abstractmethod
    async def create(self, dto: CreateAttachmentDto) -> Attachment: ...

    @abstractmethod
    async def delete(self, path: str) -> Attachment: ...
