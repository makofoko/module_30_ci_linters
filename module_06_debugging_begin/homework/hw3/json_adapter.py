import logging
import sys


class JsonAdapter(logging.LoggerAdapter):
    """
    Этот адаптер принимает сообщение (msg) и экранирует
    все символы, которые могут сломать JSON-строку:
    - Заменяет \ на \\
    - Заменяет " на \"
    """

    def process(self, msg, kwargs):
        msg_str = str(msg)

        msg_str = msg_str.replace('\\', '\\\\')
        msg_str = msg_str.replace('"', '\\"')

        return msg_str, kwargs


def setup_logging():
    """Настраивает логгер."""

    base_logger = logging.getLogger(__name__)
    base_logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler('skillbox_json_messages.log', mode='w')

    # адаптером сообщение.
    formatter = logging.Formatter(
        '{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}',
        datefmt='%H:%M:%S'
    )

    file_handler.setFormatter(formatter)

    if base_logger.hasHandlers():
        base_logger.handlers.clear()
    base_logger.addHandler(file_handler)

    return base_logger


if __name__ == '__main__':
    configured_logger = setup_logging()

    logger = JsonAdapter(configured_logger)

    # Тестируем
    logger.info('Простое сообщение.')
    logger.error('Сообщение с "двойной кавычкой".')
    logger.debug('Сообщение с C:\\Windows\\Path')
    logger.warning('Сообщение с "несколькими" \ "кавычками" и \ слешами.')