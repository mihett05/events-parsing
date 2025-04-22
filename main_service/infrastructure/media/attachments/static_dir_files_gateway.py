import os.path
from pathlib import Path

from application.attachments.gateways import FilesGateway
from domain.attachments.entities import Attachment
from domain.attachments.exceptions import (
    AttachmentAlreadyExistsError,
    AttachmentNotFoundError,
)


class StaticDirFilesGateway(FilesGateway):
    def __init__(self, base_path: Path):
        self.base_path = base_path

    async def __read(self, attachment: Attachment):
        if not os.path.exists(self.base_path / attachment.path):
            raise AttachmentNotFoundError(path=attachment.filename)

        with open(self.base_path / attachment.path, "rb") as file:
            attachment.content = file.read()

    async def __save(self, attachment: Attachment):
        if os.path.exists(self.base_path / attachment.path):
            raise AttachmentAlreadyExistsError()

        with open(self.base_path / attachment.path, "rb") as file:
            file.write(attachment.content)

    async def read(self, attachment: Attachment) -> Attachment:
        await self.__read(attachment)
        return attachment

    async def create(self, attachment: Attachment) -> Attachment:
        await self.__save(attachment)
        return attachment

    async def delete(self, attachment: Attachment) -> Attachment:
        attachment = await self.__read(attachment)
        os.remove(self.base_path / attachment.path)

        return attachment
