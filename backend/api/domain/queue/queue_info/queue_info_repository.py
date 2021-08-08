from typing import Optional
import inject
from backend.api.domain.dao import BaseDBAccessor
from backend.api.domain.queue.queue_info import QueueInfo


class QueueInfoRepository:

    @inject.params(accessor=BaseDBAccessor)
    def __init__(self, accessor: BaseDBAccessor = None):
        self.accessor = accessor

    def create(
        self,
        creator_id: int,
        course_id: int,
        group_id: int
    ) -> QueueInfo:
        with self.accessor.session() as session:
            if session.query(QueueInfo).filter_by(course_id=course_id, group_id=group_id).count() > 0:
                raise RuntimeError("QueueEntry for this course already exists for this group")

            queue = QueueInfo(
                creator_id=creator_id,
                course_id=course_id,
                group_id=group_id
            )
            session.add(queue)
            session.flush()
            session.commit()
            return queue

    def get(self,
            queue_id: int) -> Optional[QueueInfo]:
        with self.accessor.session() as session:
            queue = session.query(QueueInfo) \
                           .filter(QueueInfo.id == queue_id) \
                           .first()
            return queue
