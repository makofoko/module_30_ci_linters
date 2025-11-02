import logging
from logging_config import setup_logging

logger = logging.getLogger("service")

def main():
    logger.info("Service started")
    logger.warning("Something looks suspicious")
    logger.error("Something went wrong!")

if __name__ == "__main__":
    setup_logging()
    main()
