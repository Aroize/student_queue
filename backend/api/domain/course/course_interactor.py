from typing import List
import inject
from .cource_repository import CourseRepository
from .course import Course


class CourseInteractor:
    def __init__(self):
        self.environments = ('Discord', 'Zoom', 'IRL', 'MS Teams')

    @inject.params(course_repository=CourseRepository)
    def create(self,
               name: str,
               environment: str,
               teacher_name: str,
               course_repository: CourseRepository = None) -> Course:
        if not self._is_course_name_valid(name):
            raise ValueError('Invalid course name. Length must be greater then 2')

        if not self._is_environment_valid(environment):
            raise ValueError(f'Invalid environment. Should be one of {self.environments}')

        teacher_name = self._capitalize_teacher_name(teacher_name)
        course = course_repository.create(name, environment, teacher_name)
        return course

    @inject.params(course_repository=CourseRepository)
    def remove(self, course_id: int, course_repository: CourseRepository = None):
        course = course_repository.find_course_by_id(course_id)
        if course is None:
            raise ValueError(f'No course with id={course_id}')

        course_repository.remove(course.id)

    @inject.params(course_repository=CourseRepository)
    def find_courses_by_teacher(self, teacher_name: str, course_repository: CourseRepository = None) -> List[Course]:
        return course_repository.find_courses_by_teacher_name(teacher_name)

    @staticmethod
    def _is_course_name_valid(name: str) -> bool:
        return len(name) > 2

    @staticmethod
    def _capitalize_teacher_name(name: str) -> str:
        make_name = lambda name: name.lower().capitalize()
        return ' '.join(list(map(make_name, name.split())))

    def _is_environment_valid(self, env: str) -> bool:
        return env in self.environments

