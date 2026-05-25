#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from evaluator import Evaluator
from parse import Parser


@pytest.fixture
def parser():
    return Parser()


@pytest.fixture
def evaluator():
    return Evaluator()


@pytest.mark.parametrize(
    ("expr", "expected"),
    [
        ("2", 2.0),
        ("2 + 3", 5.0),
        ("10 - 4", 6.0),
        ("6 * 7", 42.0),
        ("8 / 2", 4.0),
        ("2 + 3 * 4", 14.0),
        ("(2 + 3) * 4", 20.0),
        ("20 / (2 * 2)", 5.0),
        ("2 + (3 + 4) * 5", 37.0),
    ],
)
def test_evaluator(parser, evaluator, expr, expected):
    tree = parser.parse(expr)
    assert evaluator.visit(tree) == expected


def test_division_by_zero(parser, evaluator):
    tree = parser.parse("10 / (5 - 5)")

    with pytest.raises(ZeroDivisionError):
        evaluator.visit(tree)
