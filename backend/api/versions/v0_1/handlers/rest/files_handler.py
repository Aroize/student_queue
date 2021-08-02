from tornado.web import StaticFileHandler
import inject
from backend.api.security import JwtTokenController
from backend.api.jrpc import InvalidAccessCredentials
from backend.api.domain.file import FileInteractor


class CustormFileHandler(StaticFileHandler):
    @inject.params(validator=JwtTokenController, file_interactor=FileInteractor)
    async def get(self, path, include_body=True, validator: JwtTokenController = None, file_interactor: FileInteractor = None):
        self.absolute_path = self.get_absolute_path(self.root, path)

        # check creds
        headers = self.request.headers
        credentials = validator.retreive_credentials(headers)

        if not validator.is_access_token_valid(credentials):
            self.set_status(404)
            return

        try:
            file_id = int(path)
        except ValueError:
            self.set_status(406)
            return

        file = file_interactor.get(file_id)
        if file is not None:
            await super(CustormFileHandler, self).get(path, include_body)
