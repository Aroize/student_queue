import inject
from backend.api.jrpc import BaseJRPCResponse, SecuredJRPCRequest, JRPCSuccessResponse
from backend.api.domain.course.lab import LabInteractor
from backend.api.versions.v0_1.handlers.base import SecuredHandler


class FindLabsByCourseHandler(SecuredHandler):
    def method(self) -> str:
        return "course.lab.find.by_course"

    # FOR DEBUG
    def need_access_token(self) -> bool:
        return False

    @inject.params(lab_interactor=LabInteractor)
    def process(self,
                payload: SecuredJRPCRequest,
                lab_interactor: LabInteractor = None) -> BaseJRPCResponse:
        course_id = payload.obtain_int('course_id')

        if course_id is None:
            return self.wrap_invalid_response("course_id parameter must be specified")

        try:
            labs = lab_interactor.find_labs_by_course(course_id)
        except Exception as e:
            return self.wrap_invalid_response(str(e))

        labs = [lab.json() for lab in labs]
        return JRPCSuccessResponse(labs, payload.id)
