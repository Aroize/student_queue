import time
import pathlib
from loguru import logger
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop

from versions import v0_1
from domain import UserInteractor, UserRepository, UserEmailConfirmationRepository
from tornado.ioloop import IOLoop
from tornado.web import Application
from security import JwtTokenController, JwtTokenControllerImpl
from mail_service import MailSenderService


class Cleaner:

    def __init__(self):
        self.period_in_sec = 24 * 60 * 60

    def __call__(self):
        # DO CLEAR HERE
        logger.info('Cleaner called')

        self.schedule()

    def schedule(self):
        IOLoop.instance().add_timeout(time.time() + self.period_in_sec, self)


class StudentQueueApp:

    def __init__(self):
        self.project_root_dir = pathlib.Path(__file__) \
                                                .resolve() \
                                                .parent \
                                                .parent \
                                                .as_posix()

    def format_tools_path(self, path: str) -> str:
        return path.format(self.project_root_dir + "/tools")

    def format_root_path(self, path: str) -> str:
        return path.format(self.project_root_dir)

    def run(self):
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
        self.settings = {
            "static_path": self.format_root_path("{}/static"),
            "static_url_prefix": "/res/"
        }

    def init_endpoints(self):
        # MAIL

        mail_sender = MailSenderService(
            self.format_tools_path("{}/smtp_config.json"),
            self.format_root_path("{}/res/email.html")
        )

        # JWT
        access_secret = self.format_tools_path("{}/certs/access_secret.json")
        refresh_secret = self.format_tools_path("{}/certs/refresh_secret.json")

        jwt_controller = JwtTokenControllerImpl(
            access_secret_file=access_secret,
            refresh_secret_file=refresh_secret
        )

        # INTERACTOR
        user_interactor = UserInteractor(UserRepository(), UserEmailConfirmationRepository(), mail_sender)

        # ENDPOINTS
        endpoints = [
            v0_1.EchoHandler(),
            v0_1.SecuredEchoHandler(),
            v0_1.RegistrationHandler(user_interactor),
            v0_1.AuthHandler(user_interactor, jwt_controller)
        ]
        method_mapping = dict(map(lambda endpoint: (endpoint.method(), endpoint), endpoints))


        # FOR EXTERNAL MAPPING
        router_params = {
            "methods": method_mapping,
            "jwt_controller": jwt_controller
        }

        email_params = {
            "user_interactor": user_interactor
        }

        self.urls = [
            ("/v0.1", v0_1.RouteHandler, router_params),
            ("/verify_email", v0_1.EmailVerificationHandler, email_params)
        ]


if __name__ == '__main__':
    app = StudentQueueApp()
    app.run()
