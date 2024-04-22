from uvicorn.config import LOGGING_CONFIG


def load_log_config():
    datefmt = '%Y-%m-%dT%H:%M:%S'
    log_fmt = '%(levelprefix)s %(asctime)s\t%(message)s'
    # default logger
    LOGGING_CONFIG['formatters']['default']['datefmt'] = datefmt
    LOGGING_CONFIG['formatters']['default']['fmt'] = log_fmt
    # access logger
    LOGGING_CONFIG['formatters']['access']['datefmt'] = datefmt
    LOGGING_CONFIG['formatters']['access']['fmt'] = log_fmt
