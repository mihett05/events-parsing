from datetime import datetime
from typing import Callable, Optional
from uuid import uuid4

import pytest

from infrastructure.api.v1.attachments.models import AttachmentModel


@pytest.fixture
def attachment_model_factory() -> Callable[[], AttachmentModel]:
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
