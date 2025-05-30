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
    """
    Реализация шлюза для работы с файлами в локальной файловой системе.

    Обеспечивает хранение файлов вложений в указанной директории,
    включая операции создания, удаления и получения ссылок на файлы.
    """

    def __init__(self, base_path: Path, prefix: str = "attachments"):
        self.base_path = base_path / prefix
        if not self.base_path.exists():
            os.makedirs(self.base_path)

    async def add_link_to_attachment(self, attachment: Attachment):
        attachment.file_link = await self.__get_link(attachment)

    async def create(self, attachment: Attachment, content: BinaryIO) -> Attachment:
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
