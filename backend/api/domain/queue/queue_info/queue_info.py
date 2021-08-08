from datetime import datetime
from backend.api.domain.dao import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey


class QueueInfo(Base):
    __tablename__ = "queue_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    creator_id = Column(Integer, ForeignKey('user.id'))
    course_id = Column(Integer, ForeignKey('course.id'))
    group_id = Column(Integer, ForeignKey('group.id'))
    registration_timestamp = Column(DateTime, default=datetime.utcnow)

    def json(self) -> dict:
        return {
            "id": self.id,
            "creator_id": self.creator_id,
            "course_id": self.course_id,
            "group_id": self.group_id,
            "registration_timestamp": self.registration_timestamp
        }

    def __repr__(self):
        return f'QueueInfo[id = {self.id}, ' \
               f'creator_id = {self.creator_id}, ' \
               f'course_id = {self.course_id}, ' \
               f'group_id = {self.group_id}, ' \
               f'registration_timestamp = {self.registration_timestamp}]'
