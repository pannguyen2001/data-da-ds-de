from functools import wraps
from typing import Callable, Optional, ParamSpec, TypeVar,  overload
import time
from src.common.logger import logger

P = ParamSpec("P")
R = TypeVar("R")


@overload
def retry(
    func: Optional[Callable[P, R]] = None,
    *,
    times: int = 3,
    delay: float = 1.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[Callable[P, R]], Callable[P, R]] | Callable[P, R]:
    """
    Retry decorator.

    Usage:

        @retry
        def foo():
            ...

        @retry(times=5)

        @retry(
            times=5,
            delay=2,
            exceptions=(TimeoutError, ConnectionError),
        )
    """
    if times < 1:
        raise ValueError("times must be >= 1")

    if delay < 0:
        raise ValueError("delay must be >= 0")

    def decorator(function: Callable[P, R]) -> Callable[P, R]:
        @wraps(function)
        def inner(*args: P.args, **kwargs: P.kwargs) -> R:
            for attempt in range(1, times + 1):
                try:
                    return function(*args, **kwargs)
                except exceptions as e:
                    logger.warning(
                        "[%s] Attempt %d/%d failed (%s): %s",
                        function.__name__,
                        attempt,
                        times,
                        type(e).__name__,
                        e,
                    )

                    if attempt == times:
                        logger.exception(
                        "[%s] All retry attempts failed.",
                        function.__name__,
                    )
                        raise

                    time.sleep(delay)

        return inner

    if func is not None:
        return decorator(func)

    return decorator



# # Complex version: kimi:
# from functools import wraps
# from typing import Callable, Optional, ParamSpec, TypeVar, Awaitable, Union
# import time
# import asyncio
# import random
# from utils.logger import other_common_logger as logger

# P = ParamSpec("P")
# R = TypeVar("R")


# class RetryExhaustedError(Exception):
#     """Raised when all attempts fail. Preserves the last exception via chaining."""

#     def __init__(self, message: str, *, attempts: int, last_exception: Exception):
#         super().__init__(message)
#         self.attempts = attempts
#         self.last_exception = last_exception


# def _validate_retry_params(
#     times: int,
#     delay: float,
#     backoff: float,
#     max_delay: Optional[float],
# ) -> None:
#     if not isinstance(times, int) or times < 1:
#         raise ValueError(f"times must be int >= 1, got {times}")
#     if delay < 0:
#         raise ValueError(f"delay must be >= 0, got {delay}")
#     if backoff < 1:
#         raise ValueError(f"backoff must be >= 1 (use 1.0 for fixed delay), got {backoff}")
#     if max_delay is not None and max_delay < delay:
#         raise ValueError(f"max_delay ({max_delay}) must be >= delay ({delay})")


# def retry(
#     func: Optional[Callable[P, R]] = None,
#     *,
#     times: int = 3,
#     delay: float = 1.0,
#     backoff: float = 2.0,
#     max_delay: Optional[float] = 10.0,
#     jitter: bool = True,
#     exceptions: tuple[type[Exception], ...] = (Exception,),
#     on_retry: Optional[Callable[[Exception, int], None]] = None,
#     wrap_final: bool = False,
# ) -> Union[Callable[[Callable[P, R]], Callable[P, R]], Callable[P, R]]:
#     """
#     Production-grade sync retry with exponential backoff and jitter.

#     @retry(times=5, backoff=2.0, max_delay=30.0, jitter=True)
#     def call_api(): ...
#     """
#     _validate_retry_params(times, delay, backoff, max_delay)

#     def decorator(function: Callable[P, R]) -> Callable[P, R]:
#         @wraps(function)
#         def inner(*args: P.args, **kwargs: P.kwargs) -> R:
#             current_delay = delay

#             for attempt in range(1, times + 1):
#                 try:
#                     return function(*args, **kwargs)
#                 except exceptions as exc:
#                     logger.warning(
#                         "[%s] attempt %d/%d failed: %s: %s",
#                         function.__name__,
#                         attempt,
#                         times,
#                         type(exc).__name__,
#                         exc,
#                     )

#                     if on_retry:
#                         try:
#                             on_retry(exc, attempt)
#                         except Exception as hook_exc:
#                             logger.error(
#                                 "[%s] on_retry hook failed: %s",
#                                 function.__name__,
#                                 hook_exc,
#                             )

#                     if attempt == times:
#                         logger.error(
#                             "[%s] all %d attempts exhausted",
#                             function.__name__,
#                             times,
#                         )
#                         if wrap_final:
#                             raise RetryExhaustedError(
#                                 f"'{function.__name__}' failed after {times} attempts",
#                                 attempts=times,
#                                 last_exception=exc,
#                             ) from exc
#                         raise

#                     sleep_for = random.uniform(0, current_delay) if jitter else current_delay
#                     time.sleep(sleep_for)

#                     next_delay = current_delay * backoff
#                     current_delay = min(next_delay, max_delay) if max_delay is not None else next_delay

#             raise RuntimeError("unreachable")  # type checker safety

#         return inner

#     if func is not None:
#         return decorator(func)
#     return decorator


# def aretry(
#     func: Optional[Callable[P, Awaitable[R]]] = None,
#     *,
#     times: int = 3,
#     delay: float = 1.0,
#     backoff: float = 2.0,
#     max_delay: Optional[float] = 10.0,
#     jitter: bool = True,
#     exceptions: tuple[type[Exception], ...] = (Exception,),
#     on_retry: Optional[Callable[[Exception, int], Awaitable[None]]] = None,
#     wrap_final: bool = False,
# ) -> Union[
#     Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]],
#     Callable[P, Awaitable[R]],
# ]:
#     """Async variant. Identical semantics, but uses asyncio.sleep and await."""
#     _validate_retry_params(times, delay, backoff, max_delay)

#     def decorator(function: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
#         @wraps(function)
#         async def inner(*args: P.args, **kwargs: P.kwargs) -> R:
#             current_delay = delay

#             for attempt in range(1, times + 1):
#                 try:
#                     return await function(*args, **kwargs)
#                 except exceptions as exc:
#                     logger.warning(
#                         "[%s] attempt %d/%d failed: %s: %s",
#                         function.__name__,
#                         attempt,
#                         times,
#                         type(exc).__name__,
#                         exc,
#                     )

#                     if on_retry:
#                         try:
#                             await on_retry(exc, attempt)
#                         except Exception as hook_exc:
#                             logger.error(
#                                 "[%s] on_retry hook failed: %s",
#                                 function.__name__,
#                                 hook_exc,
#                             )

#                     if attempt == times:
#                         logger.error(
#                             "[%s] all %d attempts exhausted",
#                             function.__name__,
#                             times,
#                         )
#                         if wrap_final:
#                             raise RetryExhaustedError(
#                                 f"'{function.__name__}' failed after {times} attempts",
#                                 attempts=times,
#                                 last_exception=exc,
#                             ) from exc
#                         raise

#                     sleep_for = random.uniform(0, current_delay) if jitter else current_delay
#                     await asyncio.sleep(sleep_for)

#                     next_delay = current_delay * backoff
#                     current_delay = min(next_delay, max_delay) if max_delay is not None else next_delay

#             raise RuntimeError("unreachable")

#         return inner

#     if func is not None:
#         return decorator(func)
#     return decorator
