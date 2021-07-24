from datetime import datetime
from ..dao import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey

class UserEmailConfirmation(Base):
    __tablename__ = "user_confirmation"

    id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    code = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return """UserEmailConfirmation[id={}, code={}]""".format(self.id, self.code)
