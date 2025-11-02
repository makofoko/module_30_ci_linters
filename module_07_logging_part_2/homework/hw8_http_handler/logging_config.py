import logging.config

dict_config = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },

    "handlers": {
        "http": {
            "class": "logging.handlers.HTTPHandler",
            "level": "INFO",
            "formatter": "base",
            "host": "localhost:5000",
            "url": "/log",
            "method": "POST"
        },
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base",
            "stream": "ext://sys.stdout"
        }
    },

    "loggers": {
        "service": {
            "level": "DEBUG",
            "handlers": ["console", "http"],
            "propagate": False
        }
    }
}

def setup_logging():
    logging.config.dictConfig(dict_config)
