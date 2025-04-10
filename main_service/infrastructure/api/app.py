import asyncio
import contextlib

from application.events.usecases import ParseEventsUseCase
from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from dishka.integrations.faststream import (
    setup_dishka as faststream_setup_dishka,
)
from domain.exceptions import EntityAlreadyExists, EntityNotFound
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from infrastructure.api.v1 import v1_router
from infrastructure.config import Config
from infrastructure.rabbit import router


async def create_rabbit_app(container: AsyncContainer) -> FastStream:
    broker = await container.get(RabbitBroker)
    broker.include_router(router)
    app = FastStream(broker)
    return app


async def parse_mails(container: AsyncContainer):
    while True:
        async with container() as request_container:
            parse = await request_container.get(ParseEventsUseCase)
            await parse()
        await asyncio.sleep(60 * 30)


def create_app(container: AsyncContainer, config: Config) -> FastAPI:
    @contextlib.asynccontextmanager
    async def lifespan(_: FastAPI):
        task = asyncio.create_task(parse_mails(container))

        rabbit_app = await create_rabbit_app(container)
        faststream_setup_dishka(container, rabbit_app, auto_inject=True)

        await rabbit_app.broker.start()
        yield

        # cancel background task
        try:
            task.cancel()
            await task
        except asyncio.CancelledError:
            pass

        await rabbit_app.broker.close()

    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,  # noqa
        allow_origins=config.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(EntityNotFound)
    async def entity_not_found_exception_handler(
        _: Request, exc: EntityNotFound
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)},
        )

    @app.exception_handler(EntityAlreadyExists)
    async def entity_already_exists_exception_handler(
        _: Request, exc: EntityAlreadyExists
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(exc)},
        )

    app.include_router(v1_router, prefix="/v1")
    setup_dishka(container, app)

    return app
