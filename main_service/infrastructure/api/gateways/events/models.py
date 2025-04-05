from infrastructure.api.models import CamelModel


class DatesInfoModel(CamelModel):
    start_date: str | None
    end_date: str | None
    end_registration: str | None


class EventInfoModel(CamelModel):
    mail_id: int
    title: str
    description: str | None
    dates: DatesInfoModel
    type: str
    format: str
    location: str | None
