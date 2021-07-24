from datetime import datetime, timezone


class NowDateTimeProvider:

    def now(self) -> datetime:
        return datetime.now(timezone.utc)
