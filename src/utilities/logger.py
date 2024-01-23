import logging

logging.basicConfig(
    format="%(asctime)s - %(levelname)s: %(message)s", level=logging.DEBUG
)


def logger_info(msg: object):
    logging.info(msg.capitalize() if isinstance(msg, str) else msg)


def logger_error(msg: object):
    logging.error(msg.capitalize() if isinstance(msg, str) else msg)
