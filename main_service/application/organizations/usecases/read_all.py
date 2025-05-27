from domain.organizations.dtos import ReadOrganizationsDto
from domain.organizations.entities import Organization
from domain.organizations.repositories import OrganizationsRepository


class ReadAllOrganizationUseCase:
    """
    Сценарий получения списка организаций.

    Предоставляет функциональность для выборки организаций
    в соответствии с заданными критериями.
    """

    def __init__(self, repository: OrganizationsRepository):
        """
        Инициализирует сценарий работы с организацией.
        """
        self.__repository = repository

    async def __call__(self, dto: ReadOrganizationsDto) -> list[Organization]:
        """
        Выполняет сценарий получения списка организаций.

        Возвращает список организаций, соответствующих критериям фильтрации.
        """
        return await self.__repository.read_all(dto)
