import collections
import re
from typing import *


class TokenizeException(Exception):
    pass


class Token(NamedTuple):
    type: str
    value: str


T_NODE_START = "node_start"
T_NODE_END = "node_end"
T_NODE_NAME = "node_name"
T_ATTR_START = "attr_start"
T_ATTR_END = "attr_end"
T_ATTR = "attr"
T_WHITESPACE = "whitespace"
T_TEXT = "text"

c = lambda s: re.compile(s, re.MULTILINE | re.DOTALL)

RULES: Dict[str, List[Tuple[str, re.Pattern, Any]]] = {
    "root": [
        (T_NODE_START, c("{"), "node"),
        (T_NODE_END, c("}"), "#pop"),
        (T_TEXT, c(r"[^{}]+"), None),
    ],
    "node": [
        (T_NODE_NAME, c(r"[a-zA-Z0-9_-]+"), None),
        (T_WHITESPACE, c(r"\s+"), ("#pop", "root")),
        (T_NODE_END, c(r"}"), "#pop"),
        (T_ATTR_START, c(r"\["), "attr"),
    ],
    "attr": [
        (T_ATTR_END, c("]"), "#pop"),
        (T_ATTR, c(r"[^\]]+"), None),
    ],
}


def tokenize(raw: str) -> Generator[Token, None, None]:
    pos, eos = 0, len(raw)

    state = ["root"]

    while pos < eos:
        for rule in RULES[state[-1]]:
            token_type, regex, new_state = rule
            match = regex.match(raw, pos)
            if match is None:
                # No match, try next rule
                continue

            yield Token(token_type, match.group(0))

            if new_state:
                if isinstance(new_state, str):
                    new_state = [new_state]
                for s in new_state:
                    if s == "#pop":
                        state.pop()
                    else:
                        state.append(s)

            start, end = match.span(0)
            pos = end
            break
        else:
            raise TokenizeException(
                f"no RE match at index {pos}, state {state}: " + raw[pos : pos + 10]
            )
    if state != ["root"]:
        raise TokenizeException("Bad tokenizer state. Do all '{' have a matching '}'?")
