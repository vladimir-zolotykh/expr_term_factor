#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator, Any
import re
from dataclasses import dataclass

expr = "2 + (3 + 4) * 5"


@dataclass
class Token:
    name: str
    val: Any


patterns: dict[str, str] = {
    k: rf"(?P<{k}>{v})"
    for k, v in {
        "NAME": r"[A-Za-z]\w*",
        "NUM": r"\d+",
        "PLUS": r"\+",
        "MINUS": r"-",
        "MUL": r"\*",
        "DIV": r"/",
        "EQ": r"=",
        "LPAREN": r"\(",
        "RPAREN": r"\)",
        "WS": r"\s+",
    }.items()
}

master_pat = "|".join(val for val in patterns.values())


def iter_tokens(expr: str) -> Iterator[Token]:
    master_pat = "|".join(val for val in patterns.values())
    for match in re.finditer(master_pat, expr):
        tok = Token(match.lastgroup, match.group(0))
        if tok.name != "WS":
            yield tok


if __name__ == "__main__":
    for tok in iter_tokens(expr):
        print(tok)
