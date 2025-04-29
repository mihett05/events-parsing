import application.notifications.usecases as use_cases
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from domain.notifications.dtos import ReadNotificationsDto
from fastapi import APIRouter

import infrastructure.api.v1.notifications.mappers as mappers
import infrastructure.api.v1.notifications.models as models

router = APIRouter(route_class=DishkaRoute, tags=["Notifications"])


@router.get("/", response_model=list[models.NotificationModel])
async def read_all_notifications(
    use_case: FromDishka[use_cases.ReadAllNotificationsUseCase],
    page: int = 0,
    page_size: int = 50,
):
    return map(
        mappers.map_to_pydantic,
        await use_case(ReadNotificationsDto(page=page, page_size=page_size)),
    )
