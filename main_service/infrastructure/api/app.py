import contextlib
import os.path

from application.auth.exceptions import InvalidCredentialsError
from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from dishka.integrations.faststream import (
    setup_dishka as faststream_setup_dishka,
)
from domain.exceptions import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
    InvalidEntityPeriodError,
)
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from faststream import FastStream
from faststream.rabbit import RabbitBroker
from starlette.staticfiles import StaticFiles

from infrastructure.api.background_tasks import (
    cancel_background_task,
    run_background_tasks,
)
from infrastructure.api.v1 import v1_router
from infrastructure.config import Config
from infrastructure.rabbit import router


async def create_rabbit_app(container: AsyncContainer) -> FastStream:
    broker = await container.get(RabbitBroker)
    broker.include_router(router)
    app = FastStream(broker)
    return app


def create_app(container: AsyncContainer, config: Config) -> FastAPI:
    @contextlib.asynccontextmanager
    async def lifespan(_: FastAPI):
        tasks = await run_background_tasks(container)

        rabbit_app = await create_rabbit_app(container)
        faststream_setup_dishka(container, rabbit_app, auto_inject=True)

        await rabbit_app.broker.start()
        yield

        # cancel background task
        await cancel_background_task(tasks)

        await rabbit_app.broker.close()

    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,  # noqa
        allow_origins=config.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(EntityNotFoundError)
    async def entity_not_found_exception_handler(
        _: Request, exc: EntityNotFoundError
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)},
        )

    @app.exception_handler(EntityAlreadyExistsError)
    async def entity_already_exists_exception_handler(
        _: Request, exc: EntityAlreadyExistsError
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(exc)},
        )

    @app.exception_handler(InvalidCredentialsError)
    async def invalid_credentials_exception_handler(
        _: Request, exc: InvalidCredentialsError
    ):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": str(exc)},
        )

    @app.exception_handler(InvalidEntityPeriodError)
    async def invalid_invalid_event_period_handler(
        _: Request, exc: InvalidEntityPeriodError
    ):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": str(exc)},
        )

    if not os.path.exists("static"):
        os.makedirs("static")

    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(v1_router, prefix="/v1")
    setup_dishka(container, app)

    return app
