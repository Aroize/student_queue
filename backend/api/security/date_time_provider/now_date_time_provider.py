from datetime import datetime, timezone
from .base_date_time_provider import BaseDateTimeProvider


class NowDateTimeProvider(BaseDateTimeProvider):

    def now(self) -> datetime:
        return datetime.now(timezone.utc)
