import inject
from backend.api.jrpc import BaseJRPCResponse, SecuredJRPCRequest, JRPCSuccessResponse
from backend.api.domain.course import CourseInteractor
from ..base import SecuredHandler


class FindCourseByTeacherHandler(SecuredHandler):
    def method(self) -> str:
        return "course.find.by_teacher"

    # FOR DEBUG
    def need_access_token(self) -> bool:
        return False

    @inject.params(course_interactor=CourseInteractor)
    def process(self,
                payload: SecuredJRPCRequest,
                course_interactor: CourseInteractor = None) -> BaseJRPCResponse:
        teacher_name = payload.obtain_str('teacher_name')

        if teacher_name is None:
            return self.wrap_invalid_response("teacher_name parameter must be specified")

        try:
            courses = course_interactor.find_courses_by_teacher(teacher_name)
        except Exception as e:
            return self.wrap_invalid_response(str(e))

        courses = [course.json() for course in courses]
        return JRPCSuccessResponse(courses, payload.id)
