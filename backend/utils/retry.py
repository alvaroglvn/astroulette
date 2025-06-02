import asyncio
import functools
from typing import (
    TypeVar,
    Callable,
    Any,
    Awaitable,
    Tuple,
    Optional,
    Type,
)

T = TypeVar("T")


def retry_async(
    max_retries: int = 3,
    delay: float = 1.0,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
    on_retry: Optional[Callable[[int, BaseException], None]] = None,
) -> Callable[[Callable[..., Awaitable[T]]], Callable[..., Awaitable[T]]]:
    """
    Retry decorator for async funcs.
    - max_retries: total attempts
    - delay: seconds between retries
    - exceptions: which exception types to catch
    - on_retry: optional callback(attempt_no, exception)
    """

    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            for attempt in range(1, max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as exc:
                    if on_retry:
                        on_retry(attempt, exc)
                    if attempt < max_retries:
                        await asyncio.sleep(delay)
                    else:
                        raise
            # if we somehow exit the loop without returning or raising:
            raise RuntimeError("retry_async: unexpected exit without result")

        return wrapper

    return decorator
