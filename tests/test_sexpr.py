#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from evaluator import Sexpr
from parse import Parser


@pytest.fixture
def parser():
    return Parser()


@pytest.fixture
def sexpr():
    return Sexpr()


@pytest.mark.parametrize(
    ("expr", "expected"),
    [
        ("2", "2"),
        ("2 + 3", "(+ 2 3)"),
        ("10 - 4", "(- 10 4)"),
        ("6 * 7", "(* 6 7)"),
        ("8 / 2", "(/ 8 2)"),
        ("2 + 3 * 4", "(+ 2 (* 3 4))"),
        ("(2 + 3) * 4", "(* (+ 2 3) 4)"),
        ("20 / (2 * 2)", "(/ 20 (* 2 2))"),
        ("2 + (3 + 4) * 5", "(+ 2 (* (+ 3 4) 5))"),
    ],
)
def test_sexpr(parser, sexpr, expr, expected):
    tree = parser.parse(expr)
    assert sexpr.visit(tree) == expected
