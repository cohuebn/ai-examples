import logging
from pythonjsonlogger import jsonlogger

from utils.config import Config


def get_log_level(value: str) -> int:
    levels = {"debug": 10, "info": 20, "warn": 30, "error": 40, "critical": 50}
    return levels.get(value.lower(), levels["info"])


def create_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    log_level = get_log_level(Config.log_level())
    logger.setLevel(log_level)
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(jsonlogger.JsonFormatter())
    logger.handlers = [log_handler]
    logger.propagate = False
    return logger
