import pathlib
from loguru import logger
from versions import v0_1
from domain import UserInteractor, UserRepository, UserEmailConfirmationRepository
from tornado.ioloop import IOLoop
from tornado.web import Application
from security import JwtTokenController, JwtTokenControllerImpl
from mail_service import MailSenderService


def create_methods_dict():
    mail_sender = MailSenderService("../tools/smtp_config.json", "./res/email.html")
    user_interactor = UserInteractor(UserRepository(), UserEmailConfirmationRepository(), mail_sender)

    endpoints = [
        v0_1.EchoHandler(),
        v0_1.SecuredEchoHandler(),
        v0_1.RegistrationHandler(user_interactor)
    ]
    return dict(map(lambda endpoint: (endpoint.method(), endpoint), endpoints))


def create_jwt_controller() -> JwtTokenController:
    access_secret = "../tools/certs/access_secret.json"
    refresh_secret = "../tools/certs/refresh_secret.json"
    return JwtTokenControllerImpl(
        access_secret_file=access_secret,
        refresh_secret_file=refresh_secret
    )


def run():

    main_router_params = {
        "methods": create_methods_dict(),
        "jwt_controller": create_jwt_controller()
    }

    urls = [
        ("/v0.1", v0_1.RouteHandler, main_router_params),
    ]

    backend_dir = pathlib.Path(__file__).resolve().parent.parent
    static_path = pathlib.PurePath(backend_dir, 'static')
    settings = {
        "static_path": static_path.as_posix(),
        "static_url_prefix": "/res/"
    }

    app = Application(urls, **settings)
    app.listen(5022)
    logger.info('Server started')
    IOLoop.instance().start()


if __name__ == '__main__':
    run()
