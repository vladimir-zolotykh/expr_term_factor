#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Callable, NoReturn, cast
import iter_tokens as IT
import parse as P


class Visitor:
    def visit(self, node: P.Node) -> float:
        self.name = f"visit{type(node).__name__}"
        func: Callable[[P.Node], float] = getattr(self, self.name, self.visit_generic)
        return func(node)

    def visit_generic(self, node: P.Node) -> NoReturn:
        raise TypeError(f"{self.__class__.__name__} has no method {self.name!r}")


class Evaluator(Visitor):
    def visitNumber(self, node: P.Node) -> float:
        return float(node.val)

    def visitPlusOp(self, node: P.Node) -> float:
        return self.visit(cast(P.Node, node.left)) + self.visit(
            cast(P.Node, node.right)
        )

    def visitMinusOp(self, node: P.Node) -> float:
        return self.visit(cast(P.Node, node.left)) - self.visit(
            cast(P.Node, node.right)
        )

    def visitMulOp(self, node: P.Node) -> float:
        return self.visit(cast(P.Node, node.left)) * self.visit(
            cast(P.Node, node.right)
        )

    def visitDivOp(self, node: P.Node) -> float:
        return self.visit(cast(P.Node, node.left)) / self.visit(
            cast(P.Node, node.right)
        )


if __name__ == "__main__":
    print(eval(IT.expr))
    expr = P.Parser().parse(IT.expr)
    print(Evaluator().visit(expr))
