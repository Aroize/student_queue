from datetime import datetime
from backend.api.domain.dao import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey


class QueueMember(Base):
    __tablename__ = "queue_member"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    lab_id = Column(Integer, ForeignKey('lab.id'))
    attempt = Column(Integer, autoincrement=True)
    posititon = Column(Integer, nullable=True)
    status = Column(Integer)
    file_id = Column(Integer, ForeignKey('file.id'), nullable=True)
    approximate_passing_time = Column(DateTime, nullable=True)
    permissions = Column(Integer)
    registration_timestamp = Column(DateTime, default=datetime.utcnow)

    def json(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "lab_id": self.lab_id,
            "attempt": self.attempt,
            "posititon": self.posititon,
            "status": self.status,
            "file_id": self.file_id,
            "approximate_passing_time": self.approximate_passing_time,
            "permissions": self.permissions,
            "registration_timestamp": self.registration_timestamp
        }

    def __repr__(self):
        return f'QueueMember[id = {self.id}, ' \
               f'user_id = {self.user_id}, ' \
               f'lab_id = {self.lab_id}, ' \
               f'attempt = {self.attempt}, ' \
               f'posititon = {self.posititon}, ' \
               f'status =  {self.status}, ' \
               f'file_id = {self.file_id}, ' \
               f'approximate_passing_time = {self.approximate_passing_time}, ' \
               f'permissions = {self.permissions}, ' \
               f'registration_timestamp = {self.registration_timestamp}]'
