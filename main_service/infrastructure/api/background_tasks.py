import asyncio

from application.events.usecases import ParseEventsUseCase
from application.mails.gateway import EmailsGateway
from application.mails.usecases import CreateMailsUseCase
from dishka import AsyncContainer

from infrastructure.api.mappers import map_mail_info_to_create_dto


async def __parse_mails(container: AsyncContainer):
    while True:
        async with container() as request_container:
            gateway = await request_container.get(EmailsGateway)
            create_many_use_case = await request_container.get(
                CreateMailsUseCase
            )
            dtos = map(
                map_mail_info_to_create_dto, await gateway.receive_mails()
            )
            await create_many_use_case(list(dtos))
        await asyncio.sleep(60 * 30)


async def __process_mails(container: AsyncContainer):
    while True:
        async with container() as request_container:
            parse = await request_container.get(ParseEventsUseCase)
            await parse()
        await asyncio.sleep(60 * 30)


async def run_background_tasks(container: AsyncContainer) -> list[asyncio.Task]:
    return [
        asyncio.create_task(__parse_mails(container)),
        asyncio.create_task(__process_mails(container)),
    ]


async def cancel_background_task(tasks: list[asyncio.Task]):
    for task in tasks:
        try:
            task.cancel()
            await task
        except asyncio.CancelledError:
            pass


__all__ = [
    "run_background_tasks",
    "cancel_background_task",
]
