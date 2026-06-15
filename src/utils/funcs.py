from datetime import datetime


def bytes_to_gb(bytes):
    return round(bytes / (1024 * 1024 * 1024), 1)

def format_date(date_input):
    if isinstance(date_input, datetime):
        dt = date_input
    elif isinstance(date_input, str):
        dt = datetime.fromisoformat(date_input)
    else:
        return str(date_input)
    
    months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]
    return f'{dt.day} {months[dt.month - 1]} {dt.year}'