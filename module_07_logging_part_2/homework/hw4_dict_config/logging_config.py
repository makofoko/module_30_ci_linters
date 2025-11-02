import logging.config
import sys

dict_config = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | line:%(lineno)d | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base",
            "stream": "ext://sys.stdout"
        },
        "debug_file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "base",
            "filename": "calc_debug.log",
            "mode": "a",
            "encoding": "utf-8"
        },
        "error_file": {
            "class": "logging.FileHandler",
            "level": "ERROR",
            "formatter": "base",
            "filename": "calc_error.log",
            "mode": "a",
            "encoding": "utf-8"
        }
    },

    "loggers": {
        "app": {
            "level": "DEBUG",
            "handlers": ["console", "debug_file", "error_file"],
            "propagate": False
        },
        "utils": {
            "level": "DEBUG",
            "handlers": ["console", "debug_file", "error_file"],
            "propagate": False
        }
    },

    "root": {
        "level": "WARNING",
        "handlers": ["console"]
    }
}


def setup_logging():
    logging.config.dictConfig(dict_config)
