from .create import CreateMailUseCase
from .create_many import CreateMailsUseCase
from .read import ReadMailUseCase
from .read_unprocessed import ReadUnprocessedMailUseCase
from .update import UpdateMailUseCase

__all__ = [
    "CreateMailUseCase",
    "ReadMailUseCase",
    "ReadUnprocessedMailUseCase",
    "UpdateMailUseCase",
    "CreateMailsUseCase",
]
