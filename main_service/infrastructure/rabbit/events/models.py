from infrastructure.api.models import CamelModel


class DatesInfoModel(CamelModel):
    start_date: str
    end_date: str | None
    end_registration: str | None


class EventInfoModel(CamelModel):
    mail_id: int | None
    title: str
    description: str | None
    dates: DatesInfoModel
    type: str
    format: str
    location: str | None
