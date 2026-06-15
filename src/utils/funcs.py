from datetime import datetime


def bytes_to_gb(bytes):
    return round(bytes / (1024 * 1024 * 1024), 1)

def format_date(timestamp: str) -> str:
    months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]
    dt = datetime.fromisoformat(timestamp)
    day = dt.day
    month_name = months[dt.month - 1]
    year = dt.year
    return f'{day} {month_name} {year}'