import logging.config
from ascii_filter import AsciiFilter, AsciiReplaceFilter

dict_config = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | line:%(lineno)d | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },

    "filters": {
        "ascii_only": {
            "()": AsciiFilter
        },
        "ascii_replace": {
            "()": AsciiReplaceFilter,
            "replacement": "ÎŒØ∏‡°⁄·°€йцукен"
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base",
            "filters": ["ascii_replace"],
            "stream": "ext://sys.stdout"
        }
    },

    "loggers": {
        "utils": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False
        },
        "__main__": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False
        }
    }
}

def setup_logging():
    logging.config.dictConfig(dict_config)