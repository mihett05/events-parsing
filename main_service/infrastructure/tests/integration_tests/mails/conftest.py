import infrastructure.gateways.mails.gateway as gateway
import pytest_asyncio
from dishka import AsyncContainer


@pytest_asyncio.fixture
async def read_messages_attachments(
        container: AsyncContainer,
) -> gateway.ImapEmailsGateway:
    async with container() as nested:
        yield await nested.get(gateway.ImapEmailsGateway)