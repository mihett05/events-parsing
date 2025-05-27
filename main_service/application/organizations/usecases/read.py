from domain.organizations.entities import Organization
from domain.organizations.repositories import OrganizationsRepository


class ReadOrganizationUseCase:
    """
    Сценарий чтения информации об организации.

    Обеспечивает получение данных организации по идентификатору.
    """

    def __init__(self, repository: OrganizationsRepository):
        """
        Инициализирует сценарий работы с организацией.
        """

        self.__repository = repository

    async def __call__(self, organization_id: int) -> Organization:
        """
        Выполняет сценарий получения организации.

        Возвращает сущность организации с указанным идентификатором.
        """
        return await self.__repository.read(organization_id)
