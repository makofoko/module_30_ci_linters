from logger_helper import get_logger
from utils import string_to_operator

logger = get_logger(__name__)

def calc(args):
    logger.info("Arguments: %s", args)
    ...