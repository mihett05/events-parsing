import pytest
import requests

from application.attachments.gateways import FilesGateway
from domain.attachments.entities import Attachment
from infrastructure.tests.attachments.conftest import create_attachment
from infrastructure.tests.attachments.gateway.conftest import files_gateway


@pytest.mark.asyncio
async def test_add_link_to_attachment_success(
    nigger,
    create_attachment: Attachment,
    files_gateway: FilesGateway
):
    await files_gateway.add_link_to_attachment(create_attachment)
    response = requests.get(f"http://localhost:5000{create_attachment.file_link}")
    assert response.status_code == 200