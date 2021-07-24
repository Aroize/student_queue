from pathlib import Path
from loguru import logger
from tornado.web import Application
from tornado.ioloop import IOLoop
import inject

from versions import v0_1
from domain import UserInteractor, UserRepository, UserEmailConfirmationRepository
from domain import GroupInteractor, GroupRepository
from security import JwtTokenControllerImpl
from mail_service import MailSenderService
from app import Cleaner


class StudentQueueApp:
    def run(self):
        self.init_dependencies()
        self.init_endpoints()
        self.init_static()

        app = Application(self.urls, **self.settings)
        app.listen(5022)
        logger.info('Server started')

        # SCHEDULE DB CLEANER [TODO(): set proper time]
        cleaner = Cleaner()
        cleaner.schedule()

        IOLoop.instance().start()

    def init_static(self):
        static_path = project_root_dir / "static"
        self.settings = {
            "static_path": static_path,
            "static_url_prefix": "/res/"
        }

    @staticmethod
    def _bind_dependencies(binder):
        # mail_sender
        binder.bind_to_constructor(MailSenderService,
                                   lambda: MailSenderService(project_root_dir / tools / "smtp_config.json",
                                                             project_root_dir / "res/email.html"))
        # jwt_controller
        binder.bind_to_constructor(JwtTokenControllerImpl,
                                   lambda: JwtTokenControllerImpl(
                                       access_secret_file=project_root_dir / tools / "certs/access_secret.json",
                                       refresh_secret_file=project_root_dir / tools / "certs/refresh_secret.json"))
        # user_repository
        binder.bind_to_constructor(UserRepository, lambda: UserRepository())
        # group_repository
        binder.bind_to_constructor(GroupRepository, lambda: GroupRepository())
        # user_interactor
        binder.bind_to_constructor(UserEmailConfirmationRepository, lambda: UserEmailConfirmationRepository())
        binder.bind_to_constructor(UserInteractor, lambda: UserInteractor(inject.instance(UserRepository),
                                                                          UserEmailConfirmationRepository(),
                                                                          inject.instance(MailSenderService)
                                                                          ))
        binder.bind_to_constructor(GroupInteractor, lambda: GroupInteractor(inject.instance(UserRepository),
                                                                            inject.instance(GroupRepository))
                                   )

    def init_dependencies(self):
        inject.configure(self._bind_dependencies)

    def init_endpoints(self):
        # ENDPOINTS
        endpoints = [
            v0_1.EchoHandler(),
            v0_1.SecuredEchoHandler(),
            v0_1.RegistrationHandler(),
            v0_1.AuthHandler(),
            v0_1.RefreshCredentialsHandler(),
            v0_1.CreateGroupHandler()
        ]
        methods_mapping = {endpoint.method(): endpoint for endpoint in endpoints}

        # not jrpc handlers
        self.urls = [
            ("/v0.1", v0_1.RouteHandler, dict(methods_mapping=methods_mapping)),
            ("/verify_email", v0_1.EmailVerificationHandler)
        ]

        logger.info("Endpoints:\n\t" + "\n\t".join([str(endpoint) for endpoint in endpoints]))


if __name__ == '__main__':
    project_root_dir = Path(__file__).resolve().parent.parent
    tools = "tools"
    app = StudentQueueApp()
    app.run()
