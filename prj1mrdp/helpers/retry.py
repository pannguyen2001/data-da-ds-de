import time
from typing import Callable
from .logger import other_common_logger

def retry(function: Callable):
    """
    Retry function until success

    Args:
        function (Callable): function to retry
        times (int, optional): number of times to retry. Defaults to 1.
        delay (int, optional): delay between retries. Defaults to 0.
        *args: arguments for function

    """
    def inner(times=1, delay=0, *args):
        while times > 0:
            try:
                return function(times, delay, *args)
            except Exception as err:
                times = times - 1
                time.sleep(delay)
                other_common_logger.error(f"[{retry.__name__} > {inner.__name__}] Execute function failed. Retry. Error: {e}.")

    return inner