# import pytest
import os

from decorator import config_tag


# @pytest.fixture(autouse=True)
# def reset_config_tag():
#     """Ensure CONFIG_TAG is reset before each test."""
#     original_tag = os.environ.get("CONFIG_TAG")
#     yield
#     if original_tag is None:
#         os.environ.pop("CONFIG_TAG", None)
#     else:
#         os.environ["CONFIG_TAG"] = original_tag


@config_tag("000")
def test_decorator():
    assert os.environ["CONFIG_TAG"] == "000"


@config_tag("000")
@config_tag("001")
def test_decorator_multiple_tags():
    # assert os.environ["CONFIG_TAG"] == "000"
    assert os.environ["CONFIG_TAG"] == "001"


# @pytest.mark.parametrize("tag, expected", [
#     ("000", "s3://incoming-000"),
#     ("001", "s3://001-incoming"),
#     ("002", "s3://my-bucket/incoming"),
# ])
# def test_decorator_parametrize(tag, expected):
#     os.environ["CONFIG_TAG"] = tag
#     assert get_config_value("s3_paths.incoming") == expected
