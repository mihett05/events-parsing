import pytest
from typing import Optional
from datetime import datetime
from uuid import uuid4

import pytest_asyncio

from infrastructure.api.v1.attachments.models import AttachmentModel
from infrastructure.api.v1.auth.models import UserWithTokenModel
from infrastructure.api.v1.users.models import UserModel



@pytest.fixture
def attachment_model_factory() -> AttachmentModel:
    def _factory(
            filename: str = "test_file.jpg",
            extension: str = ".jpg",
            file_link: str = "http://example.com/files/test.jpg",
            mail_id: Optional[int] = None,
            event_id: Optional[int] = None,
    ) -> AttachmentModel:
        return AttachmentModel(
            id=uuid4(),
            filename=filename,
            extension=extension,
            fileLink=file_link,
            mailId=mail_id,
            eventId=event_id,
            createdAt=datetime.now(),
        )

    return _factory

@pytest_asyncio.fixture
async def user_with_token_model_factory(
        user_model_factory,
        create_user_model_dto_factory,
        async_client) -> UserWithTokenModel:
    # def _factory(access_token: str = "fake-jwt-token",
    #              user: Optional[UserModel] = None) -> UserWithTokenModel:
    #     return UserWithTokenModel(accessToken=access_token,
    #                               user=user or user_model_factory())
    # return _factory

    response = await async_client.post(
        "/v1/auth/register",
        json=create_user_model_dto_factory().model_dump(by_alias=True, mode="json"),
    )
    model = UserWithTokenModel(**response.json())
    yield model
    await async_client.delete(
        "/v1/users/",
        headers={"Authorization": f"Bearer {model.access_token}"},
    )