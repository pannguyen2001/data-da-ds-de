import os
import datetime
import cProfile
import pstats
import io
from functools import wraps
from pathlib import Path
from typing import Callable
from src.common.logger import logger


today = datetime.datetime.now().strftime("%Y-%m-%d")

def profile(func: Callable):
    """
    Profile code

    Args:
        func (Callable): _description_
        output_file (str, optional): _description_. Defaults to log_path.
    """
    def decorator(f):
        @logger.catch
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Create and start profiler
            pr = cProfile.Profile()
            pr.enable()

            # Call the original function
            result = f(*args, **kwargs)

            # Stop profiling
            pr.disable()

            # Print formatted results to console
            s = io.StringIO()
            ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
            ps.print_stats(20)
            logger.info(s.getvalue())

            # Save to file if requested
            log_file = f"{today}_{f.__name__}.prf"
            log_folder = "./profile"
            log_path = os.path.join(log_folder, log_file)
            output_file = Path(log_path)
            output_file.parent.mkdir(exist_ok=True, parents=True)

            ps.dump_stats(output_file)
            logger.info(f"Profile data saved to {output_file}")

            return result
        return wrapper

    # Handle both @profile and @profile(output_file='stats.prof') syntax
    if func is None:
        return decorator
    return decorator(func)

# run file .prof: install snakeviz or tuna, and run snakeviz/tuna file.prof
