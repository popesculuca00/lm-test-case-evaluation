from concurrent.futures import ThreadPoolExecutor, TimeoutError, as_completed
from functools import wraps


def timeout(time_limit):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(func, *args, **kwargs)
                try:
                    return future.result(timeout=time_limit)
                except TimeoutError:
                    executor.shutdown(wait=False)
                    raise TimeoutError(
                        f"{func.__name__} exceeded timeout of {time_limit} seconds"
                    )
        return wrapper
    return decorator
