from datetime import datetime
from ..dao import Base
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey


class File(Base):
    __tablename__ = "file"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String)
    owner = Column(Integer, ForeignKey('user.id'))
    rules = Column(String)
    size = Column(Integer)
    upload_timestamp = Column(DateTime, default=datetime.utcnow)

    def json(self) -> dict:
        return {
            "id": self.id,
            "filename": self.filename,
            "owner": self.owner,
            "rules": self.rules,
            "size": self.size,
            "upload_timestamp": self.upload_timestamp
        }

    def __repr__(self):
        return f'File[id = {self.id}, ' \
               f'filename = {self.filename}, ' \
               f'owner = {self.owner}, ' \
               f'rules = {self.rules}, ' \
               f'size = {self.size}, ' \
               f'upload_timestamp = {self.upload_timestamp}]'
