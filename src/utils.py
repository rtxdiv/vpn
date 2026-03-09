from datetime import datetime

def format_date(timestamp):
    if timestamp <= 0: return 'Бессрочно'
    dt = datetime.fromtimestamp(timestamp / 1000)
    return dt.strftime('%d.%m.%Y')

def bytes_to_gb(bytes):
    return round(bytes / (1024 * 1024 * 1024), 1)