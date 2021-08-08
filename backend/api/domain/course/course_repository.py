from typing import Optional, List
import inject
from ..dao import BaseDBAccessor
from .course import Course


class CourseRepository:
    @inject.params(accessor=BaseDBAccessor)
    def __init__(self, accessor: BaseDBAccessor = None):
        self.accessor = accessor

    def create(self,
               name: str,
               environment: str,
               teacher_name: str) -> Course:
        with self.accessor.session() as session:
            if session.query(Course).filter_by(name=name,
                                               environment=environment,
                                               teacher=teacher_name).count() > 0:
                raise RuntimeError("Course with this name, environment and teacher name already exists")

            course = Course(name=name,
                            teacher=teacher_name,
                            environment=environment)
            session.add(course)
            session.flush()
            session.commit()
            return course

    def remove(self, course_id: int):
        with self.accessor.session() as session:
            session.query(Course).filter_by(id=course_id).delete()
            session.flush()
            session.commit()

    def get(self, course_id: int) -> Optional[Course]:
        with self.accessor.session() as session:
            return session.query(Course) \
                .filter_by(id=course_id) \
                .first()

    def get_by_teacher_name(self, query_name: str) -> List[Course]:

        def contains_in_name(teacher_name: str, query_name: str):
            for teacher_name_part in teacher_name.split():
                for query_name_part in query_name.split():
                    if teacher_name_part.startswith(query_name_part):
                        return True
            return False

        with self.accessor.session() as session:
            # "contains" method needed but not implemented in sqlalchemy
            courses = session.query(Course).all()
            courses = list(filter(lambda course: contains_in_name(course.teacher, query_name), courses))
            return courses
