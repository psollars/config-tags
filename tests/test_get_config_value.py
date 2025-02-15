import os
import pytest
from main import get_config_value


@pytest.fixture(autouse=True)
def reset_config_tag():
    yield

    os.environ.pop("CONFIG_TAG", None)


def test_get_config_value_default():
    assert get_config_value("s3_paths.incoming") == "s3://my-bucket/incoming"
    assert get_config_value("s3_paths.outgoing") == "s3://my-bucket/outgoing"
    assert get_config_value("s3_paths.nested.nested_key") == "nested_value"


def test_get_config_value_nonexistent_key():
    with pytest.raises(KeyError):
        get_config_value("s3_paths.nonexistent")
    assert get_config_value("nonexistent.key", default="top") == "top"
    assert get_config_value("s3_paths.nonexistent", default="nested") == "nested"


def test_get_config_value_tagged():
    os.environ["CONFIG_TAG"] = "000"
    assert get_config_value("s3_paths.incoming") == "s3://incoming-000"
    assert get_config_value("s3_paths.outgoing") == "s3://my-bucket/outgoing"
    assert get_config_value("s3_paths.nested.nested_key") == "nested_value"


def test_get_config_value_nonexistent_tag():
    os.environ["CONFIG_TAG"] = "nope"
    assert get_config_value("s3_paths.incoming") == "s3://my-bucket/incoming"
    assert get_config_value("s3_paths.outgoing") == "s3://my-bucket/outgoing"
    assert get_config_value("s3_paths.nested.nested_key") == "nested_value"


# def test_get_config_value_nested_tag():
#     os.environ["CONFIG_TAG"] = "001"
#     assert get_config_value("s3_paths.incoming") == "s3://001-incoming"
#     assert get_config_value("s3_paths.outgoing") == "s3://my-bucket/outgoing"


# def test_get_config_value_specific_nested_tag():
#     os.environ["CONFIG_TAG"] = "001,002"
#     assert get_config_value("s3_paths.incoming[001]") == "s3://incoming-001"
#     assert get_config_value("s3_paths.outgoing[002]") == "s3://001-outgoing-002"
