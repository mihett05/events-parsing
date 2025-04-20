from .create import CreateMailUseCase
from .read import ReadMailUseCase
from .read_unprocessed import ReadUnprocessedMailUseCase
from .update import UpdateMailUseCase
from .create_many import CreateMailsUseCase

__all__ = [
    "CreateMailUseCase",
    "ReadMailUseCase",
    "ReadUnprocessedMailUseCase",
    "UpdateMailUseCase",
    "CreateMailsUseCase"
]
