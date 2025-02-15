import os
import yaml

from decorator import config_tag

with open("config.yaml") as f:
    CONFIG = yaml.safe_load(f)

NO_DEFAULT = object()


def is_primitive(value):
    return isinstance(value, (int, float, str, bool))


def get_config_value(path, default=NO_DEFAULT):
    config_tags = os.environ.get("CONFIG_TAG", "").split(",") + [""]
    keys = path.split(".")

    def recursive_lookup(cfg, remaining_keys):
        if not remaining_keys:
            return cfg if is_primitive(cfg) else None

        key, *next_keys = remaining_keys

        for tag in config_tags:
            tagged_key = f"{key}[{tag}]" if tag else key
            if tagged_key in cfg:
                result = recursive_lookup(cfg[tagged_key], next_keys)
                if result is not None:
                    return result

        return None

    value = recursive_lookup(CONFIG, keys)

    if value is None:
        if default is NO_DEFAULT:
            raise KeyError(f"No config value found at: {path}")
        return default

    return value


@config_tag("000")
# @config_tag("001")
# @config_tag("002")
def get_buckets():
    config_tag = os.environ.get("CONFIG_TAG")
    print("config_tag:", config_tag)

    incoming = get_config_value("s3_paths.incoming")
    outgoing = get_config_value("s3_paths.outgoing")

    return incoming, outgoing


if __name__ == "__main__":
    incoming, outgoing = get_buckets()
    print("incoming:", incoming)
    print("outgoing:", outgoing)
