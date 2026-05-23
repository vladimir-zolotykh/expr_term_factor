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
    "NAME": r"(?P<NAME>[A-Za-z]\w*)",
    "NUM": r"(?P<NUM>\d+)",
    "PLUS": r"(?P<PLUS>\+)",
    "MINUS": r"(?P<MINUS>-)",
    "MUL": r"(?P<MUL>\*)",
    "DIV": r"(?P<DIV>\*)",
    "EQ": r"(?P<EQ>=)",
    "LPAREN": r"(?P<LPAREN>\()",
    "RPAREN": r"(?P<RPAREN>\))",
    "WS": r"(?P<WS>\s+)",
}

master_pat = "|".join(val for val in patterns.values())

if __name__ == "__main__":
    for m in re.finditer(master_pat, expr):
        print(m.lastgroup, m.group(0))
