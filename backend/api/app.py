from loguru import logger
from versions import v0_1
from domain import UserRepository
from tornado.ioloop import IOLoop
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from tornado.web import Application, RequestHandler
from security import JwtTokenController, JwtTokenControllerImpl


def create_methods_dict():
    endpoints = [
        v0_1.EchoHandler(),
        v0_1.SecuredEchoHandler(),
        v0_1.RegistrationHandler(UserRepository())
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

    urls = [("/v0.1", v0_1.RouteHandler, main_router_params)]

    app = Application(urls)
    app.listen(5022)
    logger.info('Server started')
    IOLoop.instance().start()

if __name__ == '__main__':
    run()
