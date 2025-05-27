from dataclasses import dataclass

from domain.mails.enums import MailStateEnum


@dataclass
class UpdateMailDto:
    """
    DTO для обновления данных почтового сообщения.

    Содержит информацию, необходимую для изменения состояния письма
    и его привязки к событию в системе.
    """

    id: int
    state: MailStateEnum
    event_id: int | None = None
