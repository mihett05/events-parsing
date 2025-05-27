from dataclasses import dataclass

from domain.users.enums import UserNotificationSendToEnum


@dataclass
class UpdateUserDto:
<<<<<<< HEAD
    """DTO для обновления данных пользователя."""
=======
    """
    Data Transfer Object для обновления данных пользователя.

    Позволяет частично обновлять информацию о пользователе.
    Все поля являются опциональными, кроме обязательного user_id.
    """
>>>>>>> cdce819a55198b003c711e6cbfdd432a5a750195

    user_id: int
    fullname: str | None = None
    telegram_id: int | None = None
    send_to_type: UserNotificationSendToEnum | None = None


@dataclass
class DeleteUserRoleDto:
<<<<<<< HEAD
    """DTO для удаления роли пользователя в организации."""
=======
    """
    Data Transfer Object для удаления роли пользователя в организации.

    Содержит идентификаторы, необходимые для однозначного определения
    связи пользователя с организацией.
    """
>>>>>>> cdce819a55198b003c711e6cbfdd432a5a750195

    user_id: int
    organization_id: int
