import json
from datetime import datetime, timedelta
from pydantic import TypeAdapter, parse_obj_as

from infrastructure.api.models import CamelModel


class DatesInfoModel(CamelModel):
    start_date: str | None
    end_date: str | None
    end_registration: str | None


class EventInfoModel(CamelModel):
    mail_id: int
    title: str | None
    description: str | None
    dates: DatesInfoModel
    type: str | None
    format: str | None
    location: str | None
