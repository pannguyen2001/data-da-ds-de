# ========== Logger wrapper ==========

from utils.logger import exception_alert_logger, waring_alert_logger
import traceback
from typing import Callable
from functools import wraps

def logger_wrapper(func: Callable) -> Callable:
    """
    Decorator to log exceptions and return None

    Args:
        func (Callable): input function

    Returns:
        Callable: function with logger
    """
    @wraps(func)
    def wrap(*args, **kwargs):
        try:
            # return func(*args, **kwargs)
            result = func(*args, **kwargs) # function should return True as default if has no return value
            if not result:
                waring_alert_logger.warning(f"[{func.__name__}] return None")
        except Exception as e:
            tb = "".join(traceback.format_exception(None, e, e.__traceback__))
            exception_alert_logger.error(f"[{func.__name__}] {e}:\n{tb}")
            raise

    return wrap
