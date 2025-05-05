from typing import Annotated
from uuid import UUID

import application.attachments.usecases as use_cases
from application.events.usecases import ReadEventUseCase
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from domain.users.entities import User
from fastapi import APIRouter, Depends, UploadFile

import infrastructure.api.v1.attachments.mappers as mappers
import infrastructure.api.v1.attachments.models as models
from infrastructure.api.models import ErrorModel
from infrastructure.api.v1.auth.deps import get_user

router = APIRouter(route_class=DishkaRoute, tags=["Attachments"])


@router.post(
    "/{event_id}",
    response_model=list[models.AttachmentModel],
    responses={404: {"model": ErrorModel}},
)
async def create_attachments(
    event_id: int,
    files: list[UploadFile],
    create_attachments_use_case: FromDishka[use_cases.CreateAttachmentUseCase],
    read_event_use_case: FromDishka[ReadEventUseCase],
    actor: Annotated[User, Depends(get_user)],
):
    event = await read_event_use_case(event_id)
    attachments, fails = await create_attachments_use_case(
        list(map(lambda file: mappers.map_file_to_dto(file, event), files)),
        actor,
    )
    return map(mappers.map_to_pydantic, attachments)


@router.get(
    "/{attachment_id}",
    response_model=models.AttachmentModel,
    responses={404: {"model": ErrorModel}},
)
async def read_attachment(
    attachment_id: UUID,
    use_case: FromDishka[use_cases.ReadAttachmentUseCase],
    actor: Annotated[User, Depends(get_user)],
):
    return mappers.map_to_pydantic(await use_case(attachment_id, actor))
