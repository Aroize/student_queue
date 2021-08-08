from datetime import datetime
from typing import List
import inject
from .lab_repository import LabRepository
from .lab import Lab


class LabInteractor:
    @inject.params(lab_repository=LabRepository)
    def create(self,
               course_id: int,
               name: str,
               number: int,
               deadline: str,
               lab_repository: LabRepository = None) -> Lab:
        if len(name) < 3:
            raise ValueError('Lab name should be longher then 3')
        if number <= 0:
            raise ValueError('Lab number should be positive integer')
        if not self._is_valid_datetime(deadline):
            raise ValueError('Deadline should be valid datetime')

        lab = lab_repository.create(course_id, name, number, deadline)
        return lab

    @staticmethod
    def _is_valid_datetime(dt: str) -> bool:
        try:
            datetime.strptime(dt, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    @inject.params(lab_repository=LabRepository)
    def find_labs_by_course(self,
                            course_id: int,
                            lab_repository: LabRepository = None) -> List[Lab]:
        labs = lab_repository.get_by_course_id(course_id)
        return labs

    @inject.params(lab_repository=LabRepository)
    def find_by_id(self,
                   lab_id: int,
                   lab_repository: LabRepository = None) -> Lab:
        lab = lab_repository.get(lab_id)
        return lab
