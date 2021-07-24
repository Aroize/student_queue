from ..dao import Base
from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint


class GroupMember(Base):
    __tablename__ = "group_member"
    __table_args__ = (
        PrimaryKeyConstraint("user_id", "group_id"),
    )

    user_id = Column(Integer, ForeignKey("user.id"))
    group_id = Column(Integer, ForeignKey("group.id"))

    def __repr__(self):
        return "Member[user={} group={}]".format(self.user_id, self.group_id)
