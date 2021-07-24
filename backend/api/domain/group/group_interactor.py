from typing import Optional, Callable
from .group import Group
from .group_repository import GroupRepository


class GroupInteractor:

    def __init__(
            self,
            user_repository: Callable,
            group_repository: GroupRepository
    ):
        self.user_repository = user_repository
        self.group_repository = group_repository

    def create(self, title: str, admin_id: int) -> Optional[Group]:

        if len(title) not in range(3, 30):
            raise ValueError("Group title length must be in range [3, 30)")

        admin = self.user_repository.find_user_by_id(admin_id)
        if admin is None:
            raise RuntimeError("User with such id doesn't exist")

        group = self.group_repository.create(title, admin.id)
        return group
