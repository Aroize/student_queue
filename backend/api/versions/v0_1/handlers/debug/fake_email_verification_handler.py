import inject
from loguru import logger
from backend.api.domain.user import UserInteractor
from backend.api.jrpc import JRPCRequest, BaseJRPCResponse, JRPCSuccessResponse, JRPCErrorResponse
from backend.api.jrpc import JRPCErrorCodes
from ..base import BaseHandler


class FakeEmailVerificationHandler(BaseHandler):

    def method(self) -> str:
        return 'debug.fake_email_verification'

    @inject.params(user_interactor=UserInteractor)
    def process(self, payload: JRPCRequest, user_interactor: UserInteractor = None) -> BaseJRPCResponse:
        id = payload.obtain_int('id')
        ok = user_interactor.fake_confirm_email(id)
        if ok:
            logger.debug(f'User with id={id} fake confirmed')
            return JRPCSuccessResponse({'confirmed': True}, payload.id)
        else:
            return JRPCErrorResponse(JRPCErrorCodes.UserNotFound.value,
                                     f'No user with id {id}',
                                     payload.id)
