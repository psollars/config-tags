import os
import yaml

from decorator import config_tag

with open("config.yaml") as f:
    CONFIG = yaml.safe_load(f)

NO_DEFAULT = object()


def get_config_value(path, default=NO_DEFAULT):
    config_tag = os.environ.get("CONFIG_TAG")
    value = CONFIG

    try:
        for key in path.split("."):
            if isinstance(value, dict):
                value = value.get(f"{key}[{config_tag}]") or value.get(key)
    except KeyError:
        if default is NO_DEFAULT:
            raise
        value = default
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
