from abc import ABCMeta, abstractmethod
from typing import BinaryIO

from domain.attachments.entities import Attachment


class FilesGateway(metaclass=ABCMeta):
    @abstractmethod
    async def create(self, attachment: Attachment, content: BinaryIO) -> Attachment: ...

    @abstractmethod
    async def add_link_to_attachment(self, attachment: Attachment): ...

    @abstractmethod
    async def delete(self, attachment: Attachment) -> Attachment: ...
