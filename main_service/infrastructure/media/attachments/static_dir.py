import os.path
from pathlib import Path
from typing import BinaryIO

from application.attachments.gateways import FilesGateway
from domain.attachments.entities import Attachment
from domain.attachments.exceptions import (
    AttachmentAlreadyExistsError,
    AttachmentNotFoundError,
)


class StaticDirFilesGateway(FilesGateway):
    def __init__(self, base_path: Path, prefix: str = "attachments"):
        self.base_path = base_path / prefix
        if not self.base_path.exists():
            os.makedirs(self.base_path)

    async def read(self, attachment: Attachment) -> Attachment:
        attachment.file_link = await self.__get_link(attachment)
        return attachment

    async def create(
        self, attachment: Attachment, content: BinaryIO
    ) -> Attachment:
        if os.path.exists(self.base_path / attachment.path):
            raise AttachmentAlreadyExistsError()

        attachment.file_link = self.base_path / attachment.path
        with open(attachment.file_link, "wb") as file:
            file.write(content.read())

        return attachment

    async def delete(self, attachment: Attachment) -> Attachment:
        os.remove(attachment.file_link)
        return attachment

    async def __get_link(self, attachment: Attachment):
        if not os.path.exists(self.base_path / attachment.path):
            raise AttachmentNotFoundError(path=attachment.filename)

        return str(self.base_path / attachment.path)
