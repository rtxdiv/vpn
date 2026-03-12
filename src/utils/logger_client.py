import logging
from pathlib import Path


def setup_loggers():
    # info logger
    info_log = logging.getLogger('info_log')
    info_log.setLevel(logging.INFO)
    
    if not info_log.handlers:
        info_handler = logging.FileHandler(Path.cwd() / 'info.log')
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        info_log.addHandler(info_handler)
    
    # error logger
    error_log = logging.getLogger('error_log')
    error_log.setLevel(logging.ERROR)
    error_log.propagate = False
    
    if not error_log.handlers:
        error_handler = logging.FileHandler(Path.cwd() / 'error.log')
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        error_log.addHandler(error_handler)
    
    return info_log, error_log

info_log, error_log = setup_loggers()