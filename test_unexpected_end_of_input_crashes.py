import pytest

from parse import Parser


@pytest.fixture
def parser():
    return Parser()


def test_unexpected_end_of_input_crashes(parser):
    """
    Demonstrates current parser bug.

    The parser crashes with AttributeError instead of raising
    a proper SyntaxError when the expression ends unexpectedly.
    """

    with pytest.raises(AttributeError):
        parser.parse("2 +")
