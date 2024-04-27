import logging
from functools import wraps
import time


def log_function_call(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.logger.debug(f"Entering {func.__name__}")
        result = func(self, *args, **kwargs)
        self.logger.debug(f"Exiting {func.__name__} with result {result}")
        return result
    return wrapper


def handle_errors(log):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                log.error(f"Failed during {func.__name__} with error: {e}")
        return wrapper
    return decorator


def notify_observers(messages):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            for message in messages:
                self.observer.notify(message)
            return result
        return wrapper
    return decorator


def measure_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.debug(f"{func.__name__} took {end_time - start_time} seconds to execute")
        return result
    return wrapper
