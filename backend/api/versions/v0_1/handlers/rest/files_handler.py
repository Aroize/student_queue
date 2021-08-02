from tornado.web import StaticFileHandler
import inject
from backend.api.security import JwtTokenControllerImpl
from backend.api.domain.file import FileInteractor

DEBUG = True
from loguru import logger
if DEBUG:
    logger.warning('DEBUG is not secured')


class FilesHandler(StaticFileHandler):
    @inject.params(validator=JwtTokenControllerImpl, file_interactor=FileInteractor)
    async def get(self,
                  path,
                  include_body=True,
                  validator: JwtTokenControllerImpl = None,
                  file_interactor: FileInteractor = None):
        # check creds
        headers = self.request.headers
        credentials = validator.retreive_credentials(headers)

        if not DEBUG:
            if not validator.is_access_token_valid(credentials):
                self.set_status(403)  # access denied
                return

        try:
            file_id = int(path)
        except ValueError:
            self.set_status(406)
            return

        file = file_interactor.get(credentials.id, file_id)
        if file is not None:
            public_filename = file.filename
            absolute_path = self.get_absolute_path(self.root, path)
            self.absolute_path = absolute_path  # tornado requirement
            # await super().get(path, include_body)
            file = open(absolute_path, 'rb').read()

            extention = public_filename.split('.')[-1]
            if file_interactor.is_picture_extention(extention):
                self.set_header("Content-Type", f"image/{extention}")
            else:
                self.set_header("Content-Type", "text/plain")

            self.set_status(200)
            self.write(file)
        else:
            self.set_status(404)

    @staticmethod
    def _is_one_picture(file: bytes) -> bool:
        return isinstance(file, bytes) and \
               len(file) > 0

    @inject.params(validator=JwtTokenControllerImpl, file_interactor=FileInteractor)
    async def post(self,
                  path,
                  include_body=True,
                  validator: JwtTokenControllerImpl = None,
                  file_interactor: FileInteractor = None):
        # check creds
        headers = self.request.headers

        credentials = validator.retreive_credentials(headers)

        if not DEBUG:
            if not validator.is_access_token_valid(credentials):
                self.set_status(403)  # access denied
                return

        file = self.request.body
        if not self._is_one_picture(file):
            self.set_status(406)  # invalid request
            return

        filename = path.split('/')[-1]
        rules = '11'
        # todo: add real rules
        try:
            file = file_interactor.create(credentials.id, rules, filename, file)
        except ValueError as e:
            return self.write({'error': str(e)})

        if file is not None:
            return self.write({'filename': file.id})
        else:
            self.set_status(418)  # I'M A TEAPOT
