#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import re
from dataclasses import dataclass

expr = "2 + (3 + 4) * 5"


@dataclass
class Token:
    pass


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

if __name__ == "__main__":
    for m in re.finditer(master_pat, expr):
        print(m.lastgroup, m.group(0))
