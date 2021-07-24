import time
from loguru import logger
from tornado.ioloop import IOLoop


class Cleaner:

    def __init__(self):
        self.period_in_sec = 24 * 60 * 60

    def __call__(self):
        # DO CLEAR HERE
        logger.info('Cleaner called')

        self.schedule()

    def schedule(self):
        IOLoop.instance().add_timeout(time.time() + self.period_in_sec, self)
