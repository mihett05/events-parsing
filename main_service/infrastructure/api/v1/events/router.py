from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

import application.events.usecases as use_cases
import infrastructure.api.v1.events.dtos as dtos
import infrastructure.api.v1.events.mappers as mappers
import infrastructure.api.v1.events.models as models
from domain.events.dtos import ReadAllEventsDto
from infrastructure.api.models import ErrorModel

router = APIRouter(route_class=DishkaRoute, tags=["Events"])


@router.get("/", response_model=list[models.EventModel])
async def read_all_events(
    use_case: FromDishka[use_cases.ReadAllEventUseCase],
    page: int = 1,
    page_size: int = 50,
):
    return map(
        lambda event: mappers.map_to_pydantic(event),
        await use_case(ReadAllEventsDto(page=page, page_size=page_size)),
    )


@router.post(
    "/",
    response_model=models.EventModel,
    responses={404: {"model": ErrorModel}},
)
async def create_event(
    dto: dtos.CreateEventModelDto,
    use_case: FromDishka[use_cases.CreateEventUseCase],
):
    return mappers.map_to_pydantic(
        await use_case(mappers.map_create_dto_from_pydantic(dto))
    )


@router.get(
    "/{event_id}",
    response_model=models.EventModel,
    responses={404: {"model": ErrorModel}},
)
async def read_event(
    event_id: int, use_case: FromDishka[use_cases.ReadEventUseCase]
):
    return mappers.map_to_pydantic(await use_case(event_id))


@router.put(
    "/{event_id}",
    response_model=models.EventModel,
    responses={404: {"model": ErrorModel}},
)
async def update_event(
    event_id: int,
    dto: dtos.UpdateEventModelDto,
    use_case: FromDishka[use_cases.UpdateEventUseCase],
):
    return mappers.map_to_pydantic(
        await use_case(
            mappers.map_update_dto_from_pydantic(dto, event_id), None
        )
    )


@router.delete(
    "/{event_id}",
    response_model=models.EventModel,
    responses={404: {"model": ErrorModel}},
)
async def delete_event(
    event_id: int,
    use_case: FromDishka[use_cases.DeleteEventUseCase],
):
    return mappers.map_to_pydantic(await use_case(event_id, None))
