from abc import ABCMeta, abstractmethod
from typing import BinaryIO

from domain.attachments.entities import Attachment


class FilesGateway(metaclass=ABCMeta):
    @abstractmethod
    async def read_link(self, attachment: Attachment) -> str: ...

    @abstractmethod
    async def read(self, attachment: Attachment) -> Attachment: ...

    @abstractmethod
    async def create(
        self, attachment: Attachment, content: BinaryIO
    ) -> Attachment: ...

    @abstractmethod
    async def delete(self, attachment: Attachment) -> Attachment: ...
