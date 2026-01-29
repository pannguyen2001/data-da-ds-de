import traceback
from functools import wraps
from typing import Callable
from utils.logger import logger


def logger_wrapper(func: Callable) -> Callable:
    @wraps(func)
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            tb = "".join(
                traceback.TracebackException.from_exception(e).format()
            )
            logger.error(
                f"""\x1b[31mError in {func.__name__}: {e}\n{tb}\x1b[0m"""
            )
            return None

    return wrap
