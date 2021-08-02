from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from backend.api.domain.dao import Base


class Lab(Base):
    __tablename__ = "lab"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('course.id'))
    name = Column(String)
    number = Column(Integer)
    deadline = Column(DateTime)
    registration_timestamp = Column(DateTime, default=datetime.utcnow)

    def json(self) -> dict:
        return {
            "id": self.id,
            "course_id": self.course_id,
            "name": self.name,
            "number": self.number,
            "deadline": str(self.deadline)
        }

    def __repr__(self):
        return f'Lab[id = {self.id}, ' \
               f'course_id = {self.course_id}' \
               f'name = {self.name}, ' \
               f'number = {self.number}' \
               f'deadline = {str(self.deadline)}, ' \
               f'timestamp = {self.registration_timestamp}]'
