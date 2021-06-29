from loguru import logger
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler

from versions import v0_1


if __name__ == '__main__':
    urls = [("/v0.1", v0_1.RouteHandler)]

    app = Application(urls)
    app.listen(5022)
    logger.info('Server started')
    IOLoop.instance().start()
