from .entities import User, UserOrganizationRole
from .enums import RoleEnum, roles_priorities_table
from .repositories import UserOrganizationRolesRepository


class RoleGetter:
    def __init__(
        self,
        roles_repository: UserOrganizationRolesRepository,
    ):
        self.__roles_repository = roles_repository

    async def __call__(
        self, user: User, organization_id: int
    ) -> UserOrganizationRole:
        roles = await self.__roles_repository.read_all(user.id)
        current = UserOrganizationRole(
            organization_id=organization_id,
            user_id=user.id,
            role=RoleEnum.PUBLIC,
        )
        for role in roles:
            current = min(
                role, current, lambda x: roles_priorities_table[x.role]
            )
        return current
