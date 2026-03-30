class PaymentInfo:
    def __init__(self, title, periods, total):
        self.title: str = title
        self.periods: dict = periods
        self.total: float = total