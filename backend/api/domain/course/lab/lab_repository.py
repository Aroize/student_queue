from datetime import datetime
from typing import Optional, List
import inject
from backend.api.domain.dao import BaseDBAccessor
from .lab import Lab


class LabRepository:
    @inject.params(accessor=BaseDBAccessor)
    def __init__(self, accessor: BaseDBAccessor = None):
        self.accessor = accessor

    def create(self,
               course_id: int,
               name: str,
               number: int,
               deadline: str) -> Lab:
        with self.accessor.session() as session:
            if session.query(Lab).filter_by(course_id=course_id,
                                            number=number).count() > 0:
                raise RuntimeError(f"Lab with number {number} already exists in course with id={course_id}")

            deadline = datetime.strptime(deadline, '%Y-%m-%d')
            lab = Lab(course_id=course_id,
                      name=name,
                      number=number,
                      deadline=deadline)
            session.add(lab)
            session.flush()
            session.commit()
            return lab

    def remove(self, course_id: int):
        raise NotImplemented

    def get(self, lab_id: int) -> Optional[Lab]:
        with self.accessor.session() as session:
            return session.query(Lab) \
                .filter_by(id=lab_id) \
                .first()

    def get_by_course_id(self, course_id: int) -> List[Lab]:
        with self.accessor.session() as session:
            labs = session.query(Lab). \
                filter_by(course_id=course_id)
            return labs
