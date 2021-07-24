from tornado.web import RequestHandler
import inject
from backend.api.domain import UserInteractor


class EmailVerificationHandler(RequestHandler):
    @inject.params(user_interactor=UserInteractor)
    def get(self, user_interactor: UserInteractor = None):
        id = int(self.get_argument('id'))
        code = int(self.get_argument('code'))

        if id is None or code is None:
            self.redirect('/res/html/failed.html')
        elif user_interactor.confirm_email(id, code):
            self.redirect('/res/html/success.html')
        else:
            self.redirect('/res/html/failed.html')

        # @Aroize, is it ok without self.write() ?
        return
