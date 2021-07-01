from loguru import logger
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler

from versions import v0_1


def create_methods_dict():
    endpoints = [
        v0_1.EchoHandler()
    ]
    return dict(map(lambda endpoint: (endpoint.method(), endpoint), endpoints))


def run():
    urls = [("/v0.1", v0_1.RouteHandler, dict(methods=create_methods_dict()))]

    app = Application(urls)
    app.listen(5022)
    logger.info('Server started')
    IOLoop.instance().start()

if __name__ == '__main__':
    run()
