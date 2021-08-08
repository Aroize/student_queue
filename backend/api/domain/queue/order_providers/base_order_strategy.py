from typing import List
from backend.api.domain.queue.queue_member import QueueMember, PassStatus



class BaseOrderStrategy:
    def reorder_by_status_change(self,
                                 members: List[QueueMember],
                                 changer_member_id: int,
                                 new_status: PassStatus) -> List[QueueMember]:
        # changes positions of members according to strategy
        # contract: members positions are already sorted by current strategy
        raise NotImplemented
