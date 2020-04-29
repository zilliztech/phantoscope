import pytest
from resource.image import Image


@pytest.fixture
def runner():
    return Image("test_name.gif", "http://test.com/123.gif", "aaaa", ["book", "history"])


def test_image_name(runner):
    assert runner.name == "test_name.gif"
    runner.name = "test_name2.gif"
    assert runner.name == "test_name2.gif"


def test_image_type(runner):
    assert runner.type == "gif"


def test_image_url(runner):
    assert runner.url == "http://test.com/123.gif"
    runner.url = "http://test.com/123456.gif"
    assert runner.url == "http://test.com/123456.gif"


def test_image_data(runner):
    assert runner.data == "aaaa"
    runner.data = "bbbb"
    assert runner.data == "bbbb"


def test_image_tags(runner):
    assert runner.tags == ["book", "history"]
    runner.tags = ["monkey", "male"]
    assert runner.tags == ["monkey", "male"]
