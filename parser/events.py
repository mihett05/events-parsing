from dataclasses import dataclass


@dataclass
class DatesInfo:
    start_date: str | None
    end_date: str | None
    end_registration: str | None


@dataclass
class EventInfo:
    title: str | None
    description: str | None
    dates: DatesInfo
    type: str | None
    format: str | None
    location: str | None
