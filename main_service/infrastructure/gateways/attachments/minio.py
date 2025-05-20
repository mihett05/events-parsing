import mimetypes
from typing import BinaryIO

from application.attachments.gateways import FilesGateway
from domain.attachments.entities import Attachment
from miniopy_async import Minio

from infrastructure.config import Config


class MinioFilesGateway(FilesGateway):
    def __init__(self, minio: Minio, config: Config):
        self.minio = minio
        self.config = config

    async def create(
        self, attachment: Attachment, content: BinaryIO
    ) -> Attachment:
        mime_type, _ = mimetypes.guess_type(attachment.path)
        await self.__create_bucket()
        await self.minio.put_object(
            self.config.minio_bucket_name,
            object_name=attachment.path,
            data=content,
            length=self.__get_binary_io_length(content),
            content_type=mime_type or "application/octet-stream",
        )
        attachment.file_link = await self.__get_link(attachment)
        return attachment

    async def add_link_to_attachment(self, attachment: Attachment):
        attachment.file_link = await self.__get_link(attachment)

    async def delete(self, attachment: Attachment):
        await self.minio.remove_object(
            self.config.minio_bucket_name, attachment.path
        )
        return attachment

    async def __create_bucket(self):
        if not await self.minio.bucket_exists(self.config.minio_bucket_name):
            await self.minio.make_bucket(self.config.minio_bucket_name)

    async def __get_link(self, attachment: Attachment):
        return await self.minio.presigned_get_object(
            bucket_name=self.config.minio_bucket_name,
            object_name=attachment.path,
        )

    @staticmethod
    def __get_binary_io_length(file: BinaryIO) -> int:
        file.seek(0, 2)
        length = file.tell()
        file.seek(0)
        return length
