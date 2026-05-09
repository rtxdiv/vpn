from database.models import UserPeriods


class PeriodsInfo:
    def __init__(self, periods, current):
        self.periods: list[UserPeriods] = periods
        self.current: UserPeriods | None = current
        self.feature_count: int = len(self.periods) - 1 if self.current else len(self.periods)