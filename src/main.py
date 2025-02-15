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
    value = CONFIG

    try:
        for key in path.split("."):
            if not isinstance(value, dict):
                break

            for tag in config_tags:
                tagged_key = f"{key}[{tag}]" if tag else key
                if tagged_key in value:
                    value = value[tagged_key]
                    if is_primitive(value):
                        return value
                    break

    except KeyError:
        pass

    if value is CONFIG or not is_primitive(value):
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
