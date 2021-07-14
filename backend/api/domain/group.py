from .dao import DBAccessor, Base
from typing import Optional, List
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, PrimaryKeyConstraint

# Tables


class Group(Base):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    admin = Column(Integer, ForeignKey("user.id"))


    @property
    def values(self):
        return {
            "id": self.id,
            "title": self.title,
            "admin": self.admin
        }

    def __repr__(self):
        return "Group[id={} admin={} title={}]".format(self.id, self.admin, self.title)


class GroupMember(Base):
    __tablename__ = "group_member"
    __table_args__ = (
        PrimaryKeyConstraint("user_id", "group_id"),
    )

    user_id = Column(Integer, ForeignKey("user.id"))
    group_id = Column(Integer, ForeignKey("group.id"))

    def __repr__(self):
        return "Member[user={} group={}]".format(self.user_id, self.group_id)


# REPOSITORY


class GroupRepository:

    def __init__(self):
        self.accessor = DBAccessor

    def update(self, group: Group):
        with self.accessor().session() as session:
            session.query(Group) \
                .filter(Group.id == group.id) \
                .update(group.values)
            session.commit()

    def create(
        self,
        title: str,
        admin_id: int
        ) -> Optional[Group]:
        with self.accessor().session() as session:
            group = Group(title=title, admin=admin_id)

            session.add(group)
            session.flush()

            admin = GroupMember(user_id=admin_id, group_id=group.id)
            session.add(admin)
            session.flush()

            session.commit()
            return group

    def add_user(
        self,
        group_id: int,
        user_id: int
        ) -> bool:
        with self.accessor().session() as session:
            is_member = session.query(GroupMember) \
                .filter(GroupMember.group_id == group_id) \
                .filter(GroupMember.user_id == user_id) \
                .count() > 0
            if is_member:
                return False

            member = GroupMember(user_id=user_id, group_id=group_id)
            session.add(member)
            session.flush()
            session.commit()

            return True

    def remove_user(
        self,
        group_id: int,
        user_id: int
        ) -> bool:
        with self.accessor().session() as session:
            group = session.query(Group) \
                .filter(Group.id == group_id) \
                .first()
            if group.admin == user_id:
                return False
            session.query(GroupMember) \
                .filter(GroupMember.group_id == group_id) \
                .filter(GroupMember.user_id == user_id) \
                .delete()
            session.commit()
            return True

    def delete_group(
        self,
        group_id: int
        ):
        with self.accessor().session() as session:
            session.query(GroupMember) \
                .filter(GroupMember.group_id == group_id) \
                .delete()
            session.query(Group) \
                .filter(Group.id == group_id) \
                .delete()
            session.commit()

    def count(
        self,
        group_id: int
        ) -> int:
        with self.accessor().session() as session:
            return session.query(GroupMember) \
                        .filter(GroupMember.group_id == group_id) \
                        .count()

    def make_admin(
        self,
        group_id: int,
        new_admin: int
        ) -> bool:
        with self.accessor().session() as session:
            new_admin_is_member = session.query(GroupMember) \
                .filter(GroupMember.group_id == group_id) \
                .filter(GroupMember.user_id == new_admin) \
                .count() > 0
            if not new_admin_is_member:
                return False
            group = session.query(Group).filter(Group.id == group_id).first()

            if group.admin == new_admin:
                return False

            group.admin = new_admin

            session.query(Group) \
                .filter(Group.id == group.id) \
                .update(group.values)

            session.commit()

            return True
