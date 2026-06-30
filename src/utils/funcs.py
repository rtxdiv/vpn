from datetime import datetime


def bytes_to_gb(bytes):
    return round(bytes / (1024 * 1024 * 1024), 1)

def format_date(date_input, time = False):
    if isinstance(date_input, datetime):
        dt = date_input
    elif isinstance(date_input, str):
        dt = datetime.fromisoformat(date_input)
    else:
        return str(date_input)
    
    months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]
    if not time:
        return f'{dt.day} {months[dt.month - 1]} {dt.year}'
    else:
        return f'{dt.day} {months[dt.month - 1]} {dt.year}, {dt.hour:02}:{dt.minute:02}'