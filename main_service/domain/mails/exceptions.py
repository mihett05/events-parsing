from domain.exceptions import (
    EntityAlreadyExistsError,
    EntityException,
    EntityNotFoundError,
)
from domain.mails.entities import Mail


class MailNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__(Mail)

    """Ошибка, которая возвращается, если mail не найден | mail/create_use_case"""


class MailAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self):
        super().__init__(Mail)

    """
    Ошибка, которая возвращается, если mail уже существует | 
    mail/create_use_case
    """


class FailedFetchMailError(EntityException):
    def __init__(self):
        super().__init__("Failed to fetch mail from inbox")

    """
    Ошибка, которая возвращается, если не удалось получить mail с помощью imap | 
    gateways/mails/gateway/ImapEmailsGateway
    """


class FailedCreateMailError(EntityException):
    def __init__(self):
        super().__init__("Failed to create mail")

    """
    Ошибка, которая возвращается, если не удалось создать mail
    """


class FailedParseMailError(EntityException):
    def __init__(self):
        super().__init__("Failed to parse mail from inbox")

    """
    Ошибка, которая возвращается, если произошла ошибка при парсинге mail | 
    gateways/mails/gateway/ImapEmailsGateway
    """
