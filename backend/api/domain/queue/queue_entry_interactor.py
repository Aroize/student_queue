from typing import List, Optional
import inject
from backend.api.domain.queue.queue_info import QueueInfo, QueueInfoInteractor
from backend.api.domain.queue.queue_member import QueueMember, QueueMemberInteractor, PassStatus
from .queue_entry_repository import QueueEntryRepository
from .queue_entry import QueueEntry
from .order_providers import LabNumberOrderStrategy


class QueueEntryInteractor:
    def __init__(self):
        self.reorder_strategy = LabNumberOrderStrategy()

    @inject.params(queue_info_interactor=QueueInfoInteractor)
    def _get_or_throw_queue_exists(self,
                                     queue_id: int,
                                     queue_info_interactor: QueueInfoInteractor = None) -> QueueInfo:
        queue = queue_info_interactor.find_by_id(queue_id)
        if queue is None:
            raise ValueError(f'QueueEntry with id={queue} not found')
        return queue

    @inject.params(queue_member_interactor=QueueMemberInteractor)
    def _get_or_throw_queue_member_exists(self,
                                            queue_member_id: int,
                                            queue_member_interactor: QueueMemberInteractor = None) -> QueueMember:
        queue_member = queue_member_interactor.find_by_id(queue_member_id)
        if queue_member is None:
            raise ValueError(f'QueueMember with id={queue_member_id} not found')
        return queue_member

    @inject.params(queue_member_interactor=QueueMemberInteractor,
                   queue_entry_repository=QueueEntryRepository)
    def set_status(self,
                   queue_id: int,
                   queue_member_id: int,
                   status: PassStatus,
                   queue_member_interactor: QueueMemberInteractor = None,
                   queue_entry_repository: QueueEntryRepository = None) -> QueueEntry:
        # Updates status of passing the lab for the given queue member
        queue = self._get_or_throw_queue_exists(queue_id)
        queue_member = self._get_or_throw_queue_member_exists(queue_member_id)

        if status == PassStatus.REGISETRED:
            if not queue_entry_repository.entry_exists(queue_id, queue_member_id):
                queue = queue_entry_repository.add(queue.id, queue_member.id)

        # explicitly reorder
        old_members = self.get_members_by_queue_id(queue_id)
        members = self.reorder_strategy.reorder_by_status_change(old_members,
                                                                 queue_member_id,
                                                                 status)
        old_members = set([member.json() for member in old_members])
        for member in members:
            if member.id == queue_member_id:
                member.status = status.value
            if member.json() not in old_members:
                # update state in db
                queue_member_interactor.set_position_and_status(member.id,
                                                                member.posititon,
                                                                member.status)
        return queue

    @inject.params(queue_info_interactor=QueueInfoInteractor,
                   queue_entry_repository=QueueEntryRepository)
    def get_members_by_queue_id(self,
                                queue_id: int,
                                queue_info_interactor: QueueInfoInteractor = None,
                                queue_entry_repository: QueueEntryRepository = None) -> Optional[List[QueueMember]]:
        queue_info = queue_info_interactor.find_by_id(queue_id)
        if queue_info is None:
            raise ValueError(f'QueueInfo with id={queue_id} not found')

        members_ids = queue_entry_repository.get_by_queue_id(queue_info.id)
        return members_ids
