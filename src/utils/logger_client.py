import logging
from pathlib import Path


def setup_loggers():
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(Path.cwd() / 'error.log')
        ]
    )
        
    info_log = logging.getLogger('info_log')
    info_log.setLevel(logging.INFO)
        
    if not info_log.handlers:
        info_handler = logging.FileHandler(Path.cwd() / 'info.log')
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        info_log.addHandler(info_handler)
        info_log.propagate = False
        
    return info_log, logging.getLogger()

info_log, error_log = setup_loggers()