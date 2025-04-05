import contextlib

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from domain.exceptions import EntityNotFound, EntityAlreadyExists
from infrastructure.api.v1 import v1_router
from infrastructure.config import Config


async def create_rabbit_app(container: AsyncContainer) -> FastStream:
    broker = await container.get(RabbitBroker)
    app = FastStream(broker)

    return app


def create_app(container: AsyncContainer, config: Config) -> FastAPI:
    @contextlib.asynccontextmanager
    async def lifespan(_: FastAPI):
        rabbit_app = await create_rabbit_app(container)
        await rabbit_app.broker.start()
        yield
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
