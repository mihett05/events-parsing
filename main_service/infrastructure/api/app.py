import contextlib
import os.path

from application.auth.exceptions import InvalidCredentialsError
from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from dishka.integrations.faststream import (
    setup_dishka as faststream_setup_dishka,
)
from domain.exceptions import (
    EntityAccessDenied,
    EntityAlreadyExistsError,
    EntityNotFoundError,
    InvalidEntityPeriodError,
)
from domain.users.exceptions import UserNotValidated
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
    """
    Создает и настраивает приложение для работы с RabbitMQ.

    Инициализирует брокер, подключает роутер и возвращает экземпляр FastStream.
    """

    broker = await container.get(RabbitBroker)
    broker.include_router(router)
    app = FastStream(broker)
    return app


def create_app(container: AsyncContainer, config: Config) -> FastAPI:
    """
    Фабрика для создания основного FastAPI-приложения.

    Настраивает жизненный цикл приложения (lifespan), CORS, обработчики ошибок,
    статические файлы и маршруты API. Также интегрирует DI-контейнер.
    """

    @contextlib.asynccontextmanager
    async def lifespan(_: FastAPI):
        """
        Контекстный менеджер для управления жизненным циклом приложения.

        Запускает фоновые задачи, инициализирует RabbitMQ-приложение,
        а также корректно завершает работу при остановке.
        """

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
    async def entity_not_found_exception_handler(_: Request, exc: EntityNotFoundError):
        """
        Обрабатывает ошибки отсутствия сущности (404 Not Found).
        """

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)},
        )

    @app.exception_handler(EntityAlreadyExistsError)
    async def entity_already_exists_exception_handler(
        _: Request, exc: EntityAlreadyExistsError
    ):
        """
        Обрабатывает ошибки дублирования сущности (400 Bad Request).
        """

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(exc)},
        )

    @app.exception_handler(EntityAccessDenied)
    async def entity_access_denied_handler(_: Request, exc: EntityAccessDenied):
        """
        Обрабатывает ошибки доступа к сущности (403 Forbidden).
        """

        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": str(exc)},
        )

    @app.exception_handler(InvalidCredentialsError)
    async def invalid_credentials_exception_handler(
        _: Request, exc: InvalidCredentialsError
    ):
        """
        Обрабатывает ошибки аутентификации (401 Unauthorized).
        """

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": str(exc)},
        )

    @app.exception_handler(InvalidEntityPeriodError)
    async def invalid_invalid_event_period_handler(
        _: Request, exc: InvalidEntityPeriodError
    ):
        """
        Обрабатывает ошибки невалидного периода сущности (422 Unprocessable Entity).
        """

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": str(exc)},
        )

    @app.exception_handler(UserNotValidated)
    async def not_activated_user(_: Request, exc: UserNotValidated):
        """
        Обрабатывает ошибки неподтвержденного пользователя (403 Forbidden).
        """

        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN, content={"message": str(exc)}
        )

    if not os.path.exists("static"):
        os.makedirs("static")

    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(v1_router, prefix="/v1")
    setup_dishka(container, app)

    return app
