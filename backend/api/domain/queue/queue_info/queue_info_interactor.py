from typing import Optional
import inject
from backend.api.domain.course import CourseInteractor
from backend.api.domain.group import GroupInteractor
from backend.api.domain.user import UserInteractor
from backend.api.domain.queue.queue_info import QueueInfo
from .queue_info_repository import QueueInfoRepository


class QueueInfoInteractor:
    @inject.params(course_interactor=CourseInteractor,
                   group_interactor=GroupInteractor,
                   user_interactor=UserInteractor,
                   queue_info_repository=QueueInfoRepository)
    def create(self,
               creator_id: int,
               course_id: int,
               group_id: int,
               course_interactor: CourseInteractor = None,
               group_interactor: GroupInteractor = None,
               user_interactor: UserInteractor = None,
               queue_info_repository: QueueInfoRepository = None) -> QueueInfo:
        user = user_interactor.find_by_id(creator_id)
        if user is None:
            raise ValueError(f'User with id={creator_id} not found')

        course = course_interactor.find_by_id(course_id)
        if course is None:
            raise ValueError(f'Course with id={course_id} not found')

        group = group_interactor.find_by_id(group_id)
        if group is None:
            raise ValueError(f'Group with id={group_id} not found')

        if not group_interactor.user_in_group(creator_id, group_id):
            raise ValueError(f'User with id={creator_id} not in group with id={group_id}')

        queue = queue_info_repository.create(creator_id, course.id, group_id)
        return queue

    @inject.params(queue_info_repository=QueueInfoRepository)
    def find_by_id(self,
                   queue_id: int,
                   queue_info_repository: QueueInfoRepository = None) -> Optional[QueueInfo]:
        return queue_info_repository.get(queue_id)
