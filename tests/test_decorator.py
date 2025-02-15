import os
import pytest

from decorator import config_tag


@pytest.fixture(autouse=True)
def reset_config_tag():
    yield

    # the decorator should clean up after itself
    assert os.environ.get("CONFIG_TAG") == None


@config_tag("000")
def test_decorator():
    assert os.environ["CONFIG_TAG"] == "000"


@config_tag("000")
@config_tag("001")
@config_tag("002")
@config_tag("003")
def test_decorator_multiple_tags():
    assert os.environ["CONFIG_TAG"] == "003,002,001,000"


@config_tag("000,001,002,003")
def test_decorator_listed_tags():
    assert os.environ["CONFIG_TAG"] == "000,001,002,003"


@config_tag("000,001")
@config_tag("002,003")
def test_decorator_listed_multiple_tags():
    assert os.environ["CONFIG_TAG"] == "002,003,000,001"


@config_tag("001")
@config_tag("001")
def test_decorator_dedupe_tags():
    assert os.environ["CONFIG_TAG"] == "001"


@config_tag("000")
def test_decorator_nested_functions():
    assert os.environ["CONFIG_TAG"] == "000"

    @config_tag("001,x")
    def nested_1():
        assert os.environ["CONFIG_TAG"] == "001,x,000"

        @config_tag("002")
        def nested_2():
            assert os.environ["CONFIG_TAG"] == "002,001,x,000"

        nested_2()

    nested_1()

    assert os.environ["CONFIG_TAG"] == "000"
