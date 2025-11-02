import logging
import operator

logger = logging.getLogger(__name__)

def string_to_operator(op):
    logger.debug("Преобразуем оператор: %s", op)
    if op == '+':
        return operator.add
    elif op == '-':
        return operator.sub
    elif op == '*':
        return operator.mul
    elif op == '/':
        return operator.truediv
    else:
        logger.error("Неизвестный оператор: %s", op)
        raise ValueError(f"Unknown operator {op}")
