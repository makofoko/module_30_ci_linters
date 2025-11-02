import logging
from operator import add, sub, mul, truediv

logger = logging.getLogger(__name__)

OPERATORS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
}

def string_to_operator(value: str):
    if not isinstance(value, str):
        logger.error("wrong operator type: %s", value)
        raise ValueError("wrong operator type")

    if value not in OPERATORS:
        logger.error("wrong operator value: %s", value)
        raise ValueError("wrong operator value")

    logger.debug("Оператор '%s' успешно преобразован", value)
    return OPERATORS[value]
