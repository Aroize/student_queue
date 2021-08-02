import inject
from backend.api.jrpc import BaseJRPCResponse, SecuredJRPCRequest, JRPCSuccessResponse
from backend.api.domain.course import CourseInteractor
from ..base import SecuredHandler


class CreateCourseHandler(SecuredHandler):
    def method(self) -> str:
        return "course.create"

    # FOR DEBUG
    def need_access_token(self) -> bool:
        return False

    @inject.params(course_interactor=CourseInteractor)
    def process(self,
                payload: SecuredJRPCRequest,
                course_interactor: CourseInteractor = None) -> BaseJRPCResponse:
        course_name = payload.obtain_str('course_name')
        teacher_name = payload.obtain_str('teacher_name')
        environment = payload.obtain_str('environment')

        if course_name is None:
            return self.wrap_invalid_response("course_name parameter must be specified")
        if teacher_name is None:
            return self.wrap_invalid_response("teacher_name parameter must be specified")
        if environment is None:
            return self.wrap_invalid_response("environment parameter must be specified")

        try:
            course = course_interactor.create(course_name, environment, teacher_name)
        except Exception as e:
            return self.wrap_invalid_response(str(e))

        return JRPCSuccessResponse(course.json(), payload.id)
