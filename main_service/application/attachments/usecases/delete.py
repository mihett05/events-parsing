from domain.attachments.entities import Attachment
from domain.users.entities import User

from application.attachments.dtos import CreateAttachmentDto
from application.attachments.gateways import FilesGateway


class DeleteAttachmentUseCase:
    def __init__(self, gateway: FilesGateway):
        self.gateway = gateway

    async def __call__(self, path: str, actor: User | None) -> Attachment:
        return await self.gateway.delete(path)
