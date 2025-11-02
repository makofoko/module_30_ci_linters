import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler

def setup_logging():
    dict_config = {
        "version": 1,
        "disable_existing_loggers": True,

        "formatters": {
            "base": {
                "format": "%(levelname)s | %(name)s | %(asctime)s | line:%(lineno)d | %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },

        "handlers": {
            "utils_file": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "level": "INFO",
                "formatter": "base",
                "filename": "utils.log",
                "when": "h",
                "interval": 10,
                "backupCount": 1,
                "encoding": "utf-8"
            }
        },

        "loggers": {
            "utils": {
                "level": "INFO",
                "handlers": ["utils_file"],
                "propagate": False
            }
        }
    }

    logging.config.dictConfig(dict_config)
