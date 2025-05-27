from abc import ABCMeta, abstractmethod
from typing import BinaryIO

from domain.attachments.entities import Attachment


class FilesGateway(metaclass=ABCMeta):
    """Абстрактный шлюз для работы с файлами вложений.

    Определяет интерфейс для операций хранения и управления файлами,
    связанными с объектами вложений.
    """

    @abstractmethod
    async def create(self, attachment: Attachment, content: BinaryIO) -> Attachment: ...

    """Создает файл вложения в хранилище."""

    @abstractmethod
    async def add_link_to_attachment(self, attachment: Attachment): ...

    """Добавляет ссылку на файл к объекту вложения."""

    @abstractmethod
    async def delete(self, attachment: Attachment) -> Attachment: ...

    """Удаляет файл вложения из хранилища."""
