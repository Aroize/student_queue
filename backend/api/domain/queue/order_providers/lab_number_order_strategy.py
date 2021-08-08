from typing import List, Tuple
from backend.api.domain.queue.queue_member import QueueMember, PassStatus
from .base_order_strategy import BaseOrderStrategy


class LabNumberOrderStrategy(BaseOrderStrategy):
    """
    Statuses order from first to last:
        1. PASSING
        2. READY/SKIP
        3. REGISTERED
        4. SUCCESS/FAILED (already passed, so they are in the end)
    Strategy keeps members with lab with smaller number before members with
    labs with bigger numbers. One user with different labs will not be placed
    after itself cause of lab number rule.
    """

    @staticmethod
    def _is_changed(members: List[QueueMember],
                    changer_member_id: int,
                    new_status: PassStatus) -> bool:
        for member in members:
            if member.id == changer_member_id:
                return member.status != new_status.value

    @staticmethod
    def _get_changer_ix(members: List[QueueMember],
                        changer_member_id: int) -> int:
        for i, member in enumerate(members):
            if member.id == changer_member_id:
                return i

    def _sort_func(self, member: QueueMember) -> Tuple[int, int, int]:
        # contract: lab with greater id will have greater number
        return member.lab_id, member.status, member.posititon

    def _remove_position_holes(self, members: List[QueueMember]) -> List[QueueMember]:
        # numerations starts from 1
        if not len(members) == members[-1].posititon:
            for i in range(1, len(members) + 1):
                members[i].posititon = i
        return members

    def reorder_by_status_change(self,
                                 members: List[QueueMember],
                                 changer_member_id: int,
                                 new_status: PassStatus
                                 ) -> List[QueueMember]:

        if not self._is_changed(members, changer_member_id, new_status):
            return members

        # order according to previous statuses positions
        members = sorted(members, key=lambda member: member.position)
        changer_ix = self._get_changer_ix(members, changer_member_id)

        if new_status == PassStatus.SKIP:
            # by default, skip 1 member
            if len(members) > changer_ix + 1 and members[changer_ix + 1].status == PassStatus.READY.value:
                p1, p2 = members[changer_ix].posititon, members[changer_ix + 1].posititon
                members[changer_ix].posititon, members[changer_ix + 1].posititon = p2, p1

        members = sorted(members, key=self._sort_func)
        members = self._remove_position_holes(members)
        return members
