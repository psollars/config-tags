import os
from functools import wraps


def config_tag(tag):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            config_tags = os.environ.get("CONFIG_TAG")
            config_tags = config_tags.split(",") if config_tags else []
            if tag not in config_tags:
                # O(n) vs O(1) for append, but you don't have to reverse the list later
                config_tags.insert(0, tag)
            os.environ["CONFIG_TAG"] = ",".join(config_tags)

            try:
                return func(*args, **kwargs)
            finally:
                config_tags.remove(tag)

                if len(config_tags) == 0:
                    os.environ.pop("CONFIG_TAG", None)
                else:
                    os.environ["CONFIG_TAG"] = ",".join(config_tags)

        return wrapper

    return decorator
