import os
from functools import wraps


def config_tag(tag):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            original_tag = os.environ.get("CONFIG_TAG")
            os.environ["CONFIG_TAG"] = tag
            try:
                return func(*args, **kwargs)
            finally:
                if original_tag is None:
                    del os.environ["CONFIG_TAG"]
                else:
                    os.environ["CONFIG_TAG"] = original_tag

        return wrapper

    return decorator
