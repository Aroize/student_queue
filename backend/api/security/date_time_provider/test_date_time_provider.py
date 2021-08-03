from datetime import datetime, timedelta
from .now_date_time_provider import NowDateTimeProvider


class TestNowDateTimeProvider(NowDateTimeProvider):

    def __init__(self, delta: timedelta):
        self.delta = delta

    def now(self) -> datetime:
        return super().now() - self.delta
