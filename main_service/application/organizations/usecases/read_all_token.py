from domain.organizations.dtos import ReadOrganizationTokensDto
from domain.organizations.entities import OrganizationToken
from domain.organizations.repositories import OrganizationTokensRepository


class ReadAllOrganizationTokensUseCase:
    """
    Сценарий получения токенов организации.

    Обеспечивает выборку токенов организации с возможностью фильтрации
    по различным параметрам.
    """
    def __init__(self, repository: OrganizationTokensRepository):
        """
        Инициализирует сценарий работы с организацией.
        """
        self.__repository = repository

    async def __call__(self, dto: ReadOrganizationTokensDto) -> list[OrganizationToken]:
        """
        Выполняет сценарий получения токенов.

        Возвращает список токенов организации, соответствующих
        заданным критериям поиска.
        """
        return await self.__repository.read_all(dto)
