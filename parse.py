#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from typing import Any
from dataclasses import dataclass
import iter_tokens as IT


@dataclass
class Node:
    val: Any

    def __repr__(self):
        csv = ", ".join(f"{v}" for k, v in self.__dict__.items() if v is not None)
        return f"{self.__class__.__name__}({csv})"


class Number(Node):
    pass


class UnaryOp(Node):
    pass


class BinaryOp(Node):
    left: Node
    right: Node
    op = ""

    def __init__(self, left, right, val=None):
        self.left = left
        self.right = right
        super().__init__(val if val else self.__class__.op)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.left}, {self.right})"


class PlusOp(BinaryOp):
    op = "+"


class MinusOp(BinaryOp):
    op = "-"


class MulOp(BinaryOp):
    op = "*"


class DivOp(BinaryOp):
    op = "/"


class Parser:
    def __init__(self):
        self.tok: IT.Token | None = None

    def parse(self, expr: str) -> Node:
        self.tokens = IT.iter_tokens(expr)
        self._advance()
        return self.expr()

    def _advance(self) -> IT.Token | None:
        """EOF is allowed"""
        try:
            self.tok = next(self.tokens)
            return self.tok
        except StopIteration:
            return None

    def _consume(self):
        """EOF is not allowed"""
        try:
            self.tok = next(self.tokens)
        except StopIteration:
            raise SyntaxError("Unexpected EOF")

    def _expect(self, expected: str) -> None:
        if self.tok and self.tok.val != expected:
            raise SyntaxError(f"{expected} is expected, got f{self.tok.val}")
        self._advance()

    def _expect_tok(self) -> IT.Token:
        if self.tok is None:
            raise SyntaxError("Unexpected EOF")
        return self.tok

    def expr(self) -> Node:
        res: Node = self.term()
        while self.tok and (op := self.tok.val) in ("+", "-"):
            self._consume()
            right = self.term()
            if op == "+":
                res = PlusOp(res, right)
            else:
                res = MinusOp(res, right)
        return res

    def term(self) -> Node:
        res: Node = self.factor()
        while self.tok and (op := self.tok.val) in ("*", "/"):
            self._consume()
            right = self.factor()
            if op == "*":
                res = MulOp(res, right)
            else:
                res = DivOp(res, right)
        return res

    def factor(self) -> Node:
        tok = self._expect_tok()
        if tok.val == "(":
            self._consume()
            res = self.expr()
            self._expect(")")
            return res
        else:
            res = Number(tok.val)
            self._advance()
            return res


if __name__ == "__main__":
    expr = Parser().parse(IT.expr)
    print(expr)
