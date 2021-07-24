from ..dao import Base
from sqlalchemy import Column, String, Integer, ForeignKey


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
