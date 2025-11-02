import logging
import sys
import os


class LevelFileHandler(logging.Handler):
    """
    Кастомный обработчик: пишет сообщения в разные файлы
    в зависимости от уровня логирования.
    """
    def __init__(self, base_filename="calc"):
        super().__init__()
        self.base_filename = base_filename
        self.formatter = logging.Formatter(
            "%(levelname)s | %(name)s | %(asctime)s | line:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        self.handlers = {
            logging.DEBUG: logging.FileHandler(f"{base_filename}_debug.log", mode="a", encoding="utf-8"),
            logging.INFO: logging.FileHandler(f"{base_filename}_info.log", mode="a", encoding="utf-8"),
            logging.WARNING: logging.FileHandler(f"{base_filename}_warning.log", mode="a", encoding="utf-8"),
            logging.ERROR: logging.FileHandler(f"{base_filename}_error.log", mode="a", encoding="utf-8"),
            logging.CRITICAL: logging.FileHandler(f"{base_filename}_critical.log", mode="a", encoding="utf-8"),
        }

        for h in self.handlers.values():
            h.setFormatter(self.formatter)

    def emit(self, record: logging.LogRecord):
        handler = self.handlers.get(record.levelno)
        if handler:
            handler.emit(record)

    def close(self):
        for h in self.handlers.values():
            h.close()
        super().close()


def get_logger(name: str):
    """
    Возвращает логгер с кастомным обработчиком LevelFileHandler
    и стандартным выводом в stdout.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(levelname)s | %(name)s | %(asctime)s | line:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    stream_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(stream_handler)
        logger.addHandler(LevelFileHandler(base_filename="calc"))

    return logger