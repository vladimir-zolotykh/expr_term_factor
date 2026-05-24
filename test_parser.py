# test_parser.py

import pytest

from parse import (
    Parser,
    Number,
    PlusOp,
    MinusOp,
    MulOp,
    DivOp,
)


@pytest.fixture
def parser():
    return Parser()


# -------------------------
# Basic number parsing
# -------------------------


def test_parse_single_number(parser):
    tree = parser.parse("42")

    assert isinstance(tree, Number)
    assert tree.val == "42"
    assert tree.left is None
    assert tree.right is None


# -------------------------
# Addition / subtraction
# -------------------------


def test_parse_addition(parser):
    tree = parser.parse("2 + 3")

    assert isinstance(tree, PlusOp)

    assert isinstance(tree.left, Number)
    assert tree.left.val == "2"

    assert isinstance(tree.right, Number)
    assert tree.right.val == "3"


def test_parse_subtraction(parser):
    tree = parser.parse("7 - 4")

    assert isinstance(tree, MinusOp)
    assert tree.left.val == "7"
    assert tree.right.val == "4"


# -------------------------
# Multiplication / division
# -------------------------


def test_parse_multiplication(parser):
    tree = parser.parse("2 * 5")

    assert isinstance(tree, MulOp)
    assert tree.left.val == "2"
    assert tree.right.val == "5"


def test_parse_division(parser):
    tree = parser.parse("20 / 4")

    assert isinstance(tree, DivOp)
    assert tree.left.val == "20"
    assert tree.right.val == "4"


# -------------------------
# Precedence
# -------------------------


def test_operator_precedence(parser):
    tree = parser.parse("2 + 3 * 4")

    # Expected:
    #       +
    #      / \
    #     2   *
    #        / \
    #       3   4

    assert isinstance(tree, PlusOp)

    assert tree.left.val == "2"

    assert isinstance(tree.right, MulOp)
    assert tree.right.left.val == "3"
    assert tree.right.right.val == "4"


def test_parentheses_override_precedence(parser):
    tree = parser.parse("(2 + 3) * 4")

    # Expected:
    #        *
    #       / \
    #      +   4
    #     / \
    #    2   3

    assert isinstance(tree, MulOp)

    assert isinstance(tree.left, PlusOp)
    assert tree.left.left.val == "2"
    assert tree.left.right.val == "3"

    assert tree.right.val == "4"


# -------------------------
# Nested expressions
# -------------------------


def test_nested_expression(parser):
    tree = parser.parse("2 + (3 + 4) * 5")

    # Expected:
    #         +
    #        / \
    #       2   *
    #          / \
    #         +   5
    #        / \
    #       3   4

    assert isinstance(tree, PlusOp)

    assert tree.left.val == "2"

    mul = tree.right
    assert isinstance(mul, MulOp)

    plus = mul.left
    assert isinstance(plus, PlusOp)

    assert plus.left.val == "3"
    assert plus.right.val == "4"

    assert mul.right.val == "5"


# -------------------------
# Left associativity
# -------------------------


def test_left_associative_addition(parser):
    tree = parser.parse("1 + 2 + 3")

    # Expected:
    #       +
    #      / \
    #     +   3
    #    / \
    #   1   2

    assert isinstance(tree, PlusOp)

    assert isinstance(tree.left, PlusOp)
    assert tree.left.left.val == "1"
    assert tree.left.right.val == "2"

    assert tree.right.val == "3"


def test_left_associative_multiplication(parser):
    tree = parser.parse("2 * 3 * 4")

    assert isinstance(tree, MulOp)

    assert isinstance(tree.left, MulOp)
    assert tree.left.left.val == "2"
    assert tree.left.right.val == "3"

    assert tree.right.val == "4"


# -------------------------
# Error handling
# -------------------------


def test_missing_closing_parenthesis(parser):
    with pytest.raises(SyntaxError):
        parser.parse("(2 + 3")


# -------------------------
# repr tests
# -------------------------


def test_number_repr():
    node = Number(None, None, "5")

    assert repr(node) == "Number(5)"


def test_binary_repr():
    tree = PlusOp(Number(None, None, "2"), Number(None, None, "3"), "+")

    assert repr(tree) == "PlusOp(Number(2), Number(3))"
