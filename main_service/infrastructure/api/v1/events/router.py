from typing import Annotated
from uuid import UUID

import application.events.usecases as use_cases
from application.auth.usecases import AuthorizeUseCase
from application.organizations.usecases import ReadAllOrganizationUseCase
from application.users.usecases import (
    CreateCalendarLinkUseCase,
    DeleteCalendarLinkUseCase,
)
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from domain.events.dtos import (
    ReadAllEventsFeedDto,
    ReadEventUsersDto,
    ReadUserEventsDto,
)
from domain.events.enums import EventFormatEnum, EventTypeEnum
from domain.organizations.dtos import ReadOrganizationsDto
from domain.users.entities import User
from fastapi import APIRouter, Depends

import infrastructure.api.v1.events.dtos as dtos
import infrastructure.api.v1.events.mappers as mappers
import infrastructure.api.v1.events.models as models
from infrastructure.api.models import ErrorModel
from infrastructure.api.v1.auth.deps import get_user
from infrastructure.api.v1.organizations.mappers import (
    map_to_pydantic as map_organization,
)
from infrastructure.config import Config

router = APIRouter(route_class=DishkaRoute, tags=["Events"])


@router.get("/", response_model=list[models.EventModel])
async def read_all_events(
    use_case: FromDishka[use_cases.ReadForFeedEventsUseCase],
    dto: dtos.ReadAllEventsFeedModelDto = Depends(),
):
    """Получение списка событий для ленты с фильтрацией и пагинацией.

    Возвращает список событий, отфильтрованных по параметрам DTO.
    """

    return map(
        mappers.map_to_pydantic,
        await use_case(mappers.map_read_all_dto_from_pydantic(dto)),
    )


@router.get("/filters", response_model=models.FilterModel)
async def get_filter_values(
    use_case: FromDishka[ReadAllOrganizationUseCase],
):
    """Получение доступных значений для фильтрации событий.

    Возвращает списки возможных типов, форматов и организаций.
    """

    return models.FilterModel(
        type=list(map(lambda x: x.value, EventTypeEnum)),
        format=list(map(lambda x: x.value, EventFormatEnum)),
        organization=list(
            map(
                map_organization,
                await use_case(ReadOrganizationsDto(page=None, page_size=None)),
            )
        ),
    )


@router.post("/subscribe/ical")
async def create_ical(
    use_case: FromDishka[CreateCalendarLinkUseCase],
    config: FromDishka[Config],
    actor: Annotated[User, Depends(get_user)],
):
    """Создание ссылки для подписки на календарь событий в формате iCal.

    Генерирует уникальную ссылку для текущего пользователя.
    """

    return await use_case(config.base_url, actor)


@router.delete("/subscribe/ical")
async def delete_ical(
    use_case: FromDishka[DeleteCalendarLinkUseCase],
    actor: Annotated[User, Depends(get_user)],
):
    """Удаление ссылки на подписку календаря.

    Отменяет ранее сгенерированную подписку для текущего пользователя.
    """

    return await use_case(actor)


@router.get(
    "/subscribe/ical/{uuid}",
    responses={404: {"model": ErrorModel}},
)
async def read_ical(
    use_case: FromDishka[use_cases.ReadICSUseCase],
    uuid: UUID,
):
    """Получение событий в формате iCalendar по UUID подписки."""

    return mappers.map_to_ics(await use_case(uuid))


@router.get("/subscribe/my", response_model=list[models.EventModel])
async def read_for_user(
    use_case: FromDishka[use_cases.ReadUserEventsUseCase],
    actor: Annotated[User, Depends(get_user)],
    page: int = 0,
    page_size: int = 50,
):
    """Получение событий текущего пользователя с пагинацией."""

    return map(
        mappers.map_to_pydantic,
        await use_case(
            ReadUserEventsDto(user_id=actor.id, page=page, page_size=page_size)
        ),
    )


@router.get(
    "/subscribe/{event_id}",
    response_model=list[models.UserModel],
    responses={404: {"model": ErrorModel}},
)
async def read_subscribers(
    event_id: int,
    use_case: FromDishka[use_cases.ReadEventUsersUseCase],
    actor: Annotated[User, Depends(get_user)],
    page: int = 0,
    page_size: int = 50,
):
    """Получение списка подписчиков события с пагинацией."""

    return map(
        mappers.map_to_user,
        await use_case(
            ReadEventUsersDto(event_id=event_id, page=page, page_size=page_size),
            actor,
        ),
    )


@router.post(
    "/subscribe/{event_id}",
    response_model=models.EventUserModel,
    responses={404: {"model": ErrorModel}},
)
async def subscribe(
    event_id: int,
    use_case: FromDishka[use_cases.CreateEventUserUseCase],
    actor: Annotated[User, Depends(get_user)],
):
    """Подписка текущего пользователя на указанное событие."""

    return mappers.event_user_map_to_pydantic(await use_case(event_id, actor))


@router.delete(
    "/subscribe/{event_id}",
    response_model=models.EventUserModel,
    responses={404: {"model": ErrorModel}},
)
async def unsubscribe(
    event_id: int,
    use_case: FromDishka[use_cases.DeleteEventUserUseCase],
    actor: Annotated[User, Depends(get_user)],
):
    """Отписка текущего пользователя от указанного события."""

    return mappers.event_user_map_to_pydantic(await use_case(event_id, actor))


@router.post(
    "/",
    response_model=models.EventModel,
    responses={404: {"model": ErrorModel}},
)
async def create_event(
    dto: dtos.CreateEventModelDto,
    use_case: FromDishka[use_cases.CreateEventUseCase],
    actor: Annotated[User, Depends(get_user)],
):
    """Создание нового события."""

    return mappers.map_to_pydantic(
        await use_case(mappers.map_create_dto_from_pydantic(dto), actor)
    )


@router.get(
    "/{event_id}",
    response_model=models.EventModel,
    responses={404: {"model": ErrorModel}},
)
async def read_event(
    event_id: int,
    use_case: FromDishka[use_cases.ReadEventUseCase],
    actor: Annotated[User, Depends(get_user)],
):
    """Получение информации о конкретном событии."""

    return mappers.map_to_pydantic(await use_case(event_id, actor))


@router.put(
    "/{event_id}",
    response_model=models.EventModel,
    responses={404: {"model": ErrorModel}},
)
async def update_event(
    event_id: int,
    dto: dtos.UpdateEventModelDto,
    use_case: FromDishka[use_cases.UpdateEventUseCase],
    actor: Annotated[User, Depends(get_user)],
):
    """Обновление информации о событии."""

    return mappers.map_to_pydantic(
        await use_case(mappers.map_update_dto_from_pydantic(dto, event_id), actor)
    )


@router.delete(
    "/{event_id}",
    response_model=models.EventModel,
    responses={404: {"model": ErrorModel}},
)
async def delete_event(
    event_id: int,
    use_case: FromDishka[use_cases.DeleteEventUseCase],
    actor: Annotated[User, Depends(get_user)],
):
    """Удаление события."""

    return mappers.map_to_pydantic(await use_case(event_id, actor))
