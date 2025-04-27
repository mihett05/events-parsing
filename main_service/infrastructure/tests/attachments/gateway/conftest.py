import os
import shutil

import pytest_asyncio
from dishka import AsyncContainer
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from application.attachments.gateways import FilesGateway
from application.attachments.usecases import ReadAttachmentUseCase


@pytest_asyncio.fixture
async def files_gateway(
    container: AsyncContainer,
) -> FilesGateway:
    async with container() as nested:
        yield await nested.get(FilesGateway)


@pytest_asyncio.fixture
async def read_attachment_usecase(
    container: AsyncContainer,
) -> ReadAttachmentUseCase:
    async with container() as nested:
        yield await nested.get(ReadAttachmentUseCase)





@pytest_asyncio.fixture
async def nigger(create_app: FastAPI):
    from uvicorn import run

    run(create_app, port=5000, host="0.0.0.0")
