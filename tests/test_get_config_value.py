import os
import pytest
import yaml
from main import get_config_value


@pytest.fixture
def config():
    with open("config.yaml", encoding="utf-8") as f:
        CONFIG = yaml.safe_load(f)
    return CONFIG


@pytest.fixture(autouse=True)
def reset_config_tag():
    yield

    os.environ.pop("CONFIG_TAG", None)


def test_get_config_value_default(config):
    assert get_config_value(config, "s3_paths.incoming") == "s3://my-bucket/incoming"
    assert get_config_value(config, "s3_paths.outgoing") == "s3://my-bucket/outgoing"
    assert get_config_value(config, "s3_paths.nested.nested_key") == "nested_value"


def test_get_config_value_nonexistent_key(config):
    with pytest.raises(KeyError):
        get_config_value(config, "s3_paths.nonexistent")
    assert get_config_value(config, "nonexistent.key", default="top") == "top"
    assert (
        get_config_value(config, "s3_paths.nonexistent", default="nested") == "nested"
    )


def test_get_config_value_tagged(config):
    os.environ["CONFIG_TAG"] = "000"
    assert get_config_value(config, "s3_paths.incoming") == "s3://incoming-000"
    assert get_config_value(config, "s3_paths.outgoing") == "s3://my-bucket/outgoing"
    assert get_config_value(config, "s3_paths.nested.nested_key") == "nested_value"


def test_get_config_value_nonexistent_tag(config):
    os.environ["CONFIG_TAG"] = "nope"
    assert get_config_value(config, "s3_paths.incoming") == "s3://my-bucket/incoming"
    assert get_config_value(config, "s3_paths.outgoing") == "s3://my-bucket/outgoing"
    assert get_config_value(config, "s3_paths.nested.nested_key") == "nested_value"


def test_get_config_value_top_and_nested(config):
    os.environ["CONFIG_TAG"] = "001"
    assert get_config_value(config, "s3_paths.incoming") == "s3://001-incoming"
    assert get_config_value(config, "s3_paths.outgoing") == "s3://my-bucket/outgoing"
    assert get_config_value(config, "s3_paths.nested.nested_key") == "nested_value"


def test_get_config_value_specific_nested_tag(config):
    os.environ["CONFIG_TAG"] = "002,001"
    assert get_config_value(config, "s3_paths.incoming") == "s3://001-incoming"
    assert get_config_value(config, "s3_paths.outgoing") == "s3://001-outgoing-002"
    assert get_config_value(config, "s3_paths.nested.nested_key") == "nested_value"


def test_get_config_value_primitives():
    config = {
        "primitive_values": {
            "integer": 42,
            "float": 3.14,
            "boolean": True,
            "string": "hello",
            "integer[001]": 99,
            "boolean[002]": False,
        }
    }

    os.environ["CONFIG_TAG"] = "001,002"
    # Tagged int override
    assert get_config_value(config, "primitive_values.integer") == 99
    # Untagged float
    assert get_config_value(config, "primitive_values.float") == 3.14
    # Tagged bool override
    assert get_config_value(config, "primitive_values.boolean") is False
    # Untagged string
    assert get_config_value(config, "primitive_values.string") == "hello"


def test_get_config_value_deeply_nested_tagged():
    config = {
        "deeply": {
            "nested": {
                "value": "untagged",
                "value[001]": "tagged-001",
            },
            "nested[001]": {"different_key": "nested-key-001"},
        }
    }

    os.environ["CONFIG_TAG"] = "001"
    # Should return the tagged value
    assert get_config_value(config, "deeply.nested.value") == "tagged-001"
    # Inherited tag lookup
    assert get_config_value(config, "deeply.nested.different_key") == "nested-key-001"
    # Default fallback
    assert get_config_value(config, "deeply.nested.missing_key", default="fb") == "fb"


def test_get_config_value_partial_tagging():
    config = {
        "service": {
            "url": "https://default.service.com",
            "url[001]": "https://tagged-001.service.com",
            "nested": {"key": "nested-default"},
            "nested[002]": {"key": "nested-tagged-002"},
        }
    }

    os.environ["CONFIG_TAG"] = "002,001"
    # Should use 001 for 'url'
    assert get_config_value(config, "service.url") == "https://tagged-001.service.com"
    # Should use 002 for 'nested.key'
    assert get_config_value(config, "service.nested.key") == "nested-tagged-002"


def test_get_config_value_missing_keys():
    config = {"exists": "value"}

    os.environ["CONFIG_TAG"] = "001"
    with pytest.raises(KeyError):
        get_config_value(config, "missing.key")

    assert get_config_value(config, "missing.key", default="fallback") == "fallback"


def test_get_config_value_empty_values():
    config = {
        "empty_cases": {
            "empty": "",
            "none": None,
            "override[001]": "override",
        }
    }

    os.environ["CONFIG_TAG"] = "001"
    # Empty string should be returned
    assert get_config_value(config, "empty_cases.empty") == ""
    # None should fall back
    assert get_config_value(config, "empty_cases.none", default="fb") == "fb"
    # Tagged value should take priority
    assert get_config_value(config, "empty_cases.override") == "override"


def test_get_config_value_list_handling():
    config = {
        "services": [
            {"name": "service1", "url": "https://service1.com"},
            {"name": "service2", "url": "https://service2.com"},
        ]
    }

    os.environ["CONFIG_TAG"] = "001"
    with pytest.raises(KeyError):
        # Lists should not be accessed like dicts
        get_config_value(config, "services.name")

    assert get_config_value(config, "services") == config["services"]




