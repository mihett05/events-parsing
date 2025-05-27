import asyncio
from datetime import date, datetime, timedelta
from typing import Any, Callable, Coroutine

from application.events.usecases import (
    ParseEventsUseCase,
    PlanningEventsNotificationsUseCase,
)
from application.mails.gateway import EmailsGateway
from application.mails.usecases import CreateMailsUseCase
from application.notifications.usecases import ProcessUnsentNotificationsUseCase
from dishka import AsyncContainer

from infrastructure.api.mappers import map_mail_info_to_create_dto


def background_task_runner(
    delay: timedelta,
) -> Callable[
    [Callable[..., Coroutine[Any, Any, Any]]],
    Callable[[AsyncContainer], Coroutine[Any, Any, None]],
]:
    """Декоратор для создания фоновых задач с заданным интервалом выполнения."""

    def _runner(func: Callable[..., Coroutine[..., ..., ...]]):
        async def _wrapper(container: AsyncContainer):
            while True:
                _ = await func(container)
                await asyncio.sleep(delay.total_seconds())

        return _wrapper

    return _runner


@background_task_runner(delay=timedelta(days=1))
async def __notifications_sender(container: AsyncContainer):
    """Фоновая задача для отправки непрочитанных уведомлений."""

    async with container() as request_container:
        use_case = await request_container.get(ProcessUnsentNotificationsUseCase)
        await use_case()


@background_task_runner(delay=timedelta(days=1))
async def __notifications_list_planning(container: AsyncContainer):
    """
    Фоновая задача для планирования уведомлений о событиях.

    Ежедневно создает уведомления для событий, которые должны произойти
    в ближайшие дни (сегодня, завтра и через 5 дней).
    """

    async def _task(event_start_date: datetime, notification_send_date: date):
        async with container() as request_container:
            use_case = await request_container.get(PlanningEventsNotificationsUseCase)
            await use_case(event_start_date, notification_send_date)

    # Планирование рассылки за один день до, поэтому сдвиг на timedelta(days=1)
    now = datetime.now().date()
    send_offset = timedelta(days=1)
    deltas = (timedelta(days=0), timedelta(days=1), timedelta(days=5))
    await asyncio.gather(
        *map(
            lambda delta: _task(now + delta + send_offset, now + send_offset),
            deltas,
        )
    )


@background_task_runner(delay=timedelta(minutes=30))
async def __parse_mails(container: AsyncContainer):
    """
    Фоновая задача для обработки входящих писем.

    Каждые 30 минут получает новые письма, преобразует их во внутренний формат
    и отмечает неудачные попытки обработки.
    """

    async with container() as request_container:
        gateway = await request_container.get(EmailsGateway)
        create_many_use_case = await request_container.get(CreateMailsUseCase)

        dtos = map(map_mail_info_to_create_dto, await gateway.receive_mails())
        _, need_to_retry = await create_many_use_case(list(dtos), None)

        await gateway.mark_mails_as_failed(need_to_retry)


@background_task_runner(delay=timedelta(minutes=30))
async def __process_mails(container: AsyncContainer):
    """
    Фоновая задача для парсинга событий из писем.

    Каждые 30 минут обрабатывает сохраненные письма для извлечения информации
    о событиях.
    """

    async with container() as request_container:
        parse = await request_container.get(ParseEventsUseCase)
        await parse()


async def run_background_tasks(container: AsyncContainer) -> list[asyncio.Task]:
    """
    Запускает все фоновые задачи приложения.

    Возвращает список созданных задач для последующего управления их жизненным циклом.
    """

    return [
        asyncio.create_task(__notifications_list_planning(container)),
        asyncio.create_task(__notifications_sender(container)),
        asyncio.create_task(__parse_mails(container)),
        asyncio.create_task(__process_mails(container)),
    ]


async def cancel_background_task(tasks: list[asyncio.Task]):
    """
    Корректно останавливает все фоновые задачи.

    Последовательно отменяет каждую задачу и обрабатывает возможные ошибки отмены.
    """

    for task in tasks:
        try:
            task.cancel()
            await task
        except asyncio.CancelledError:
            continue


__all__ = [
    "run_background_tasks",
    "cancel_background_task",
]
