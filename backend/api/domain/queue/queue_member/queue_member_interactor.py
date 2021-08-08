from typing import Optional
import inject
from backend.api.domain.file import FileInteractor
from backend.api.domain.user import UserInteractor
from backend.api.domain.course.lab import LabInteractor
from .queue_member import QueueMember
from .queue_member_repository import QueueMemberRepository
from .pass_status import PassStatus


class QueueMemberInteractor:
    @inject.params(file_interactor=FileInteractor,
                   user_interactor=UserInteractor,
                   lab_interactor=LabInteractor,
                   queue_member_repository=QueueMemberRepository)
    def create(self,
               user_id: int,
               lab_id: int,
               file_id: int,
               file_interactor: FileInteractor = None,
               user_interactor: UserInteractor = None,
               lab_interactor: LabInteractor = None,
               queue_member_repository: QueueMemberRepository = None) -> QueueMember:
        user = user_interactor.find_by_id(user_id)
        if user is None:
            raise ValueError(f'User with id={user_id} not found')

        lab = lab_interactor.find_by_id(lab_id)
        if lab is None:
            raise ValueError(f'Lab with id={lab_id} not found')

        file = file_interactor.get(user_id, file_id)
        if file is None:
            raise ValueError(f'File with id={file_id} not found or not accessible')

        # todo: make thread-safety
        # position doesnt available before user set up READY status
        new_user_position = None
        approximate_passing_time = None
        permissions = None  # todo
        new_user_status = PassStatus.REGISETRED.value

        queue_member = queue_member_repository.create(user.id,
                                                      lab.id,
                                                      new_user_position,
                                                      new_user_status,
                                                      file.id,
                                                      approximate_passing_time,
                                                      permissions)

        return queue_member

    @inject.params(queue_member_repository=QueueMemberRepository)
    def find_by_id(self,
                   member_id: int,
                   queue_member_repository: QueueMemberRepository = None) -> Optional[QueueMember]:
        return queue_member_repository.get(member_id)

    @inject.params(queue_member_repository=QueueMemberRepository)
    def set_position_and_status(self,
                     member_id: int,
                     position: int,
                     status: int,
                     queue_member_repository: QueueMemberRepository = None):
        q_member = queue_member_repository.get(member_id)
        q_member.posititon = position
        q_member.status = status
        queue_member_repository.update(q_member)
