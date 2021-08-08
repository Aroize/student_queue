from typing import Optional, List, Any
import inject
from backend.api.domain.dao import BaseDBAccessor
from .queue_entry import QueueEntry


class QueueEntryRepository:

    @inject.params(accessor=BaseDBAccessor)
    def __init__(self, accessor: BaseDBAccessor = None):
        self.accessor = accessor

    def add(
        self,
        queue_id: int,
        queue_member_id: int
    ) -> QueueEntry:
        with self.accessor.session() as session:
            queue = QueueEntry(queue_id=queue_id,
                               queue_member_id=queue_member_id)
            session.add(queue)
            session.flush()
            session.commit()
            return queue

    def entry_exists(self, queue_info_id: int, queue_member_id: int) -> bool:
        with self.accessor.session() as session:
            queue_entry = session.query(QueueEntry) \
                                 .filter(QueueEntry.queue_id == queue_info_id,
                                         QueueEntry.queue_member_id == queue_member_id) \
                                 .first()
            return queue_entry is not None

    def get_by_queue_id(self, queue_info_id: int) -> List[QueueEntry]:
        with self.accessor.session() as session:
            queue_entries = session.query(QueueEntry) \
                                   .filter(QueueEntry.queue_id == queue_info_id) \
                                   .all()
            return queue_entries
