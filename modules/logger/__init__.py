import logging
import logging.config
from functools import wraps

from aiogram import types


config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "custom": {
            "format": "{asctime} - {levelname} - {message}",
            "style": "{",
            "datefmt": "%d/%m %H:%M:%S",
            "encoding": "UTF-8"
        }
    },
    "handlers": {
        "stdout": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "custom"
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs.log",
            "formatter": "custom",
            # "mode": "a"
        }
    },
    "loggers": {
        "custom_std": {
            "handlers": ["stdout"],
            "level": "INFO",
            "propagate": True
        },
        "file": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True
        }
    }
}

logging.config.dictConfig(config)
logger = logging.getLogger('file')
logger.addHandler(logging.StreamHandler())


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        message: types.Message = args[0]
        if message.chat.id == message.from_user.id:
            logger.info(f"{message.from_user.id} - {message.text}")
        else:
            logger.info(
                f"{message.from_user.id} / {message.chat.id} - {message.text}")
        return func(*args, **kwargs)
    return wrapper
