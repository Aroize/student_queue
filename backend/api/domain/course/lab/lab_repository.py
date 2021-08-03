from datetime import datetime
from typing import Optional, List
from backend.api.domain.dao import DBAccessor
from .lab import Lab


class LabRepository:
    def __init__(self):
        self.accessor = DBAccessor

    def create(self,
               course_id: int,
               name: str,
               number: int,
               deadline: str) -> Lab:
        with self.accessor().session() as session:
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

    def find_lab_by_id(self, lab_id: int) -> Optional[Lab]:
        with self.accessor().session() as session:
            return session.query(Lab) \
                .filter_by(id=lab_id) \
                .first()

    def find_labs_by_course_id(self, course_id: int) -> List[Lab]:
        with self.accessor().session() as session:
            labs = session.query(Lab). \
                filter_by(course_id=course_id)
            return labs
