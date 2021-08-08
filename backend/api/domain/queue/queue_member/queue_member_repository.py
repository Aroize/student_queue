from typing import Optional, List, Any
import inject
from backend.api.domain.dao import BaseDBAccessor
from .queue_member import QueueMember
from .pass_status import PassStatus


class QueueMemberRepository:

    @inject.params(accessor=BaseDBAccessor)
    def __init__(self, accessor: BaseDBAccessor = None):
        self.accessor = accessor

    def _is_attempt_failed(self, attempt: QueueMember) -> bool:
        return attempt.status == PassStatus.FAILED.value

    def create(
        self,
        user_id: int,
        lab_id: int,
        position: Optional[int],
        status: Optional[int],
        file_id: Optional[int],
        approximate_passing_time: Optional[str],
        permissions: Optional[int]
    ) -> QueueMember:
        with self.accessor.session() as session:
            attempts = session.query(QueueMember).filter_by(user_id=user_id, lab_id=lab_id).all()
            if len(attempts) and not all(map(self._is_attempt_failed, attempts)):
                raise RuntimeError("Cant create new queue member. User havent failed his previous attempt(s)")

            queue_member = QueueMember(
                user_id=user_id,
                lab_id=lab_id,
                attempt=len(attempts) + 1,
                position=position,
                status=status,
                file_id=file_id,
                approximate_passing_time=approximate_passing_time,
                permissions=permissions
            )
            session.add(queue_member)
            session.flush()
            session.commit()
            return queue_member

    def update(self,
               queue_member: QueueMember):
        # should update only last attempt
        with self.accessor.session() as session:
            last_attempt = session.query(QueueMember) \
                                  .filter_by(user_id=queue_member.user_id,
                                             lab_id=queue_member.lab_id) \
                                  .last()
            if last_attempt is None:
                raise RuntimeError(f"QueueMember with user_id={queue_member.user_id} and lab_id={queue_member.lab_id} not found")

            last_attempt.update(queue_member.values)
            session.commit()

    def get(self, member_id: int) -> Optional[QueueMember]:
        with self.accessor.session() as session:
            q_member = session.query(QueueMember) \
                              .filter(QueueMember.id == member_id) \
                              .first()
            return q_member
