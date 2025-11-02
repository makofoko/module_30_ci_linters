import logging
from dict_config import setup_logging

setup_logging()

logger = logging.getLogger("appLogger")

def main():
    logger.debug("Debug message (увидишь в файле)")
    logger.info("Info message (увидишь в файле)")
    logger.warning("Warning message (увидишь и в консоли, и в файле)")
    logger.error("Error message (увидишь и там, и там)")

if __name__ == "__main__":
    main()
