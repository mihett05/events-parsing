from dataclasses import dataclass


@dataclass
class DatesInfo:
    start_date: str | None
    end_date: str | None
    end_registration: str | None


@dataclass
class EventInfo:
    mail_id: int | None
    title: str
    description: str | None
    dates: DatesInfo
    type: str
    format: str
    location: str | None
