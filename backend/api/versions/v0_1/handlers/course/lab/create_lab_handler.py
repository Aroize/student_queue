import inject
from backend.api.jrpc import BaseJRPCResponse, SecuredJRPCRequest, JRPCSuccessResponse
from backend.api.domain.course.lab import LabInteractor
from backend.api.versions.v0_1.handlers.base import SecuredHandler


class CreateLabHandler(SecuredHandler):
    def method(self) -> str:
        return "course.lab.create"

    # FOR DEBUG
    def need_access_token(self) -> bool:
        return False

    @inject.params(lab_interactor=LabInteractor)
    def process(self,
                payload: SecuredJRPCRequest,
                lab_interactor: LabInteractor = None) -> BaseJRPCResponse:
        course_id = payload.obtain_int('course_id')
        number = payload.obtain_int('number')
        name = payload.obtain_str('name')
        deadline = payload.obtain_str('deadline')

        for param, param_name in zip([course_id, number, name, deadline],
                                     ['course_id', 'number', 'name', 'deadline']):
            if param is None:
                return self.wrap_invalid_response(f"{param_name} parameter must be specified")

        try:
            lab = lab_interactor.create(course_id, name, number, deadline)
        except Exception as e:
            return self.wrap_invalid_response(str(e))

        return JRPCSuccessResponse(lab.json(), payload.id)
