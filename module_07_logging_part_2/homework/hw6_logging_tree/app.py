import sys
import logging
from utils import string_to_operator
from logging_tree import printout

logger = logging.getLogger(__name__)

def calc(args):
    logger.info("Arguments: %s", args)

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
    except ValueError as e:
        logger.error("Error while converting number 1: %s", e)
        return

    try:
        num_2 = float(num_2)
    except ValueError as e:
        logger.error("Error while converting number 2: %s", e)
        return

    operator_func = string_to_operator(operator)
    result = operator_func(num_1, num_2)

    logger.info("Result: %s", result)
    logger.debug("%s %s %s = %s", num_1, operator, num_2, result)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s | %(name)s | %(asctime)s | line:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout
    )

    calc(['2', '+', '3'])
    printout()

    from logging_tree.format import build_description
    with open("logging_tree.txt", "w", encoding="utf-8") as f:
        f.write(build_description())


