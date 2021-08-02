import inject
from backend.api.jrpc import BaseJRPCResponse, SecuredJRPCRequest, JRPCSuccessResponse
from backend.api.domain.course import CourseInteractor
from ..base import SecuredHandler


class RemoveCourseHandler(SecuredHandler):
    def method(self) -> str:
        return "course.remove"

    # FOR DEBUG
    def need_access_token(self) -> bool:
        return False

    @inject.params(course_interactor=CourseInteractor)
    def process(self,
                payload: SecuredJRPCRequest,
                course_interactor: CourseInteractor = None) -> BaseJRPCResponse:
        course_id = payload.obtain_int('course_id')

        if course_id is None:
            return self.wrap_invalid_response("course_id parameter must be specified")

        try:
            course_interactor.remove(course_id)
        except Exception as e:
            return self.wrap_invalid_response(str(e))

        return JRPCSuccessResponse({'status': 'removed'}, payload.id)
