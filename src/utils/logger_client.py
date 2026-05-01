import logging
from pathlib import Path


def setup_loggers():
    log_dir = Path.cwd() / 'logs'
    log_dir.mkdir(exist_ok=True, parents=True)

    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'error.log')
        ]
    )
        
    info_log = logging.getLogger('info_log')
    info_log.setLevel(logging.INFO)
        
    if not info_log.handlers:
        info_handler = logging.FileHandler(log_dir / 'info.log')
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        info_log.addHandler(info_handler)
        info_log.propagate = False
        
    return info_log, logging.getLogger()

info_log, error_log = setup_loggers()