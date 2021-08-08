from backend.api.domain.dao import Base
from sqlalchemy import Column, Integer, ForeignKey


class QueueEntry(Base):
    __tablename__ = "queue_entry"

    queue_id = Column(Integer, ForeignKey('queue_info.id'))
    queue_member_id = Column(Integer, ForeignKey('queue_member.id'))

    def json(self) -> dict:
        return {
            "queue_id": self.queue_id,
            "queue_member_id": self.queue_member_id
        }

    def __repr__(self):
        return f'QueueEntry[queue_id = {self.queue_id}, ' \
               f'queue_member_id = {self.queue_member_id}]'
