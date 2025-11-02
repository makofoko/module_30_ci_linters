import logging
import sys

def setup_logging():
    """
    Конфигурирует логирование для всего приложения.
    Вывод в stdout, формат:
    уровень | логгер | время | номер строки | сообщение
    """
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(levelname)s | %(name)s | %(asctime)s | line:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[handler]
    )