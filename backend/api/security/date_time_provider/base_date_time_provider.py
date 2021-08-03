from datetime import datetime


class BaseDateTimeProvider:
    def now(self) -> datetime:
        raise NotImplemented
