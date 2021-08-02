from datetime import datetime
from ..dao import Base
from sqlalchemy import Column, String, Integer, DateTime, Boolean


class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    teacher = Column(String)
    environment = Column(String)
    registration_timestamp = Column(DateTime, default=datetime.utcnow)

    def json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "environment": self.environment,
            "teacher": self.teacher
        }

    def __repr__(self):
        return f'Course[id = {self.id}, ' \
               f'name = {self.name}, ' \
               f'environment = {self.environment}' \
               f'teacher = {self.teacher}, ' \
               f'timestamp = {self.registration_timestamp}]'
