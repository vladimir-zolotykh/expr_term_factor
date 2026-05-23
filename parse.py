#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from types import Any
from dataclasses import dataclass
import iter_tokens as IT


@dataclass
class Node:
    left: Node
    right: Node
    val: Any


class Number(Node):
    pass


class UnaryOp(Node):
    pass


class BinaryOp(Node):
    pass


class PlusOp(BinaryOp):
    pass


class MinusOp(BinaryOp):
    pass


class MulOp(BinaryOp):
    pass


class DivOp(BinaryOp):
    pass


class Parser:
    def parse(self, expr) -> Node:
        self.tokens = IT.iter_tokens(expr)
        self._advance()
        return self.expr()

    def _advance(self) -> IT.Token:
        self.token, self.tok = self.tok, next(self.tokes)
        return self.tok

    def _consume(self):
        self.token, self.tok = self.tok, next(self.tokes)

    def _expect(self, expected: str) -> None:
        if self.tok.val != expected:
            raise SyntaxError(f"{expected} is expected, got f{self.tok.val}")
        self._consume()

    def expr(self) -> Node:
        left: Node = self.term()
        while self.tok.val in ("+", "-"):
            op = self.tok
            self._consume()
            right = self.term()
            if op == "+":
                res = PlusOp(left, right)
            else:
                res = MinusOp(left, right)
        return res

    def term(self) -> Node:
        left: Node = self.factor()
        while self.tok.val in ("*", "/"):
            op = self.tok
            self._consume()
            right = self.factor()
            if op == "*":
                res = MulOp(left, right)
            else:
                res = DivOp(left, right)
        return res

    def factor(self) -> Node:
        if self.tok.val == "(":
            self._consume()
            res = self.expr()
            self._expect(")")
            return res
        else:
            return Number(self.tok.val)
