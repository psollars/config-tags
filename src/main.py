import os
from typing import Union
import yaml
from decorator import config_tag


NO_DEFAULT = object()


def get_config_value(
    config: dict[str, Union[dict, list, int, float, str, bool]],
    path: str,
    default=NO_DEFAULT,
):
    config_tags = os.environ.get("CONFIG_TAG", "").split(",") + [""]
    keys = path.split(".")

    def recursive_lookup(cfg, remaining_keys):
        if not remaining_keys:
            return cfg

        key, *next_keys = remaining_keys

        for tag in config_tags:
            tagged_key = f"{key}[{tag}]" if tag else key
            if tagged_key in cfg:
                result = recursive_lookup(cfg[tagged_key], next_keys)
                if result is not None:
                    return result

        return None

    value = recursive_lookup(config, keys)

    if value is None:
        if default is NO_DEFAULT:
            raise KeyError(f"No config value found at: {path}")
        return default

    return value


@config_tag("000")
@config_tag("001")
@config_tag("002")
def get_buckets():
    config_tags = os.environ.get("CONFIG_TAG")
    print("config_tags:", config_tags)

    with open("config.yaml", encoding="utf-8") as f:
        CONFIG = yaml.safe_load(f)

    i = get_config_value(CONFIG, "s3_paths.incoming")
    o = get_config_value(CONFIG, "s3_paths.outgoing")

    return i, o


if __name__ == "__main__":
    incoming, outgoing = get_buckets()
    print("incoming:", incoming)
    print("outgoing:", outgoing)
