from typing import Optional
import inject
from ..user import UserRepository
from .group import Group
from .group_repository import GroupRepository


class GroupInteractor:
    @inject.params(user_repository=UserRepository,
                   group_repository=GroupRepository)
    def create(self,
               title: str,
               admin_id: int,
               user_repository: UserRepository = None,
               group_repository: GroupRepository = None) -> Optional[Group]:

        if len(title) not in range(3, 30):
            raise ValueError("Group title length must be in range [3, 30)")

        admin = user_repository.find_user_by_id(admin_id)
        if admin is None:
            raise RuntimeError("User with such id doesn't exist")

        group = group_repository.create(title, admin.id)
        return group

    @inject.params(group_repository=GroupRepository)
    def find_by_id(self, group_id: int, group_repository: GroupRepository = None) -> Optional[Group]:
        return group_repository.get(group_id)

    @inject.params(group_repository=GroupRepository)
    def user_in_group(self,
                      user_id: int,
                      group_id: int,
                      group_repository: GroupRepository = None
                      ) -> bool:
        return group_repository.contains(group_id, user_id)
