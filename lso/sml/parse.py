from typing import Any, List, Optional, Dict

import lso.sml.tokenize as T


class ParseException(Exception):
    pass


class Node(object):

    """Represents a node in the document tree."""

    name: str
    children: List["Node"]
    attr: Dict[str, Any]

    def __init__(self, name: str, children=None, **kw):
        self.name = name
        self.children = children or []
        self.attr = kw

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.__dict__ == other.__dict__

    def __repr__(self):
        child_repr = " ".join(repr(x) for x in self.children)
        if self.attr:
            attr_inner = " ".join(f"{k}={v}" for k, v in self.attr.items())
            attr_repr = f"[{attr_inner}]"
        else:
            attr_repr = ""
        return f"({self.name}{attr_repr} {child_repr})"

    def pretty_print(self, indent=""):
        if self.name == "TEXT":
            print(indent + f'({self.name} "{self.value}")')
            return
        print(indent + f"({self.name}")
        for child in self.children:
            child.pretty_print(indent + "  ")
        print(indent + ")")


class Text(Node):
    """Special node for plain text."""

    NAME = "TEXT"

    def __init__(self, value):
        Node.__init__(self, Text.NAME)
        self.value = value

    def __repr__(self):
        return f"({self.name} {self.value})"


def parse(raw: str) -> Node:
    stack = [Node("document")]
    for token in T.tokenize(raw):
        if token.type == T.T_NODE_START:
            # Name will be set once node name is seen.
            stack.append(Node("", []))

        elif token.type == T.T_NODE_NAME:
            stack[-1].name = token.value

        elif token.type == T.T_NODE_END:
            last = stack.pop()
            # Ignore surrounding whitespace so braces can
            # be laid out as the user prefers.
            if isinstance(last, Text):
                last.value = last.value.strip()

            if not last.name:
                raise ParseException("Node is missing a name.")
            if not stack:
                raise ParseException("Found '}' without matching '{'")
            stack[-1].children.append(last)

        elif token.type == T.T_ATTR:
            for item in token.value.split():
                # TODO: hack for attributes
                k, _, v = item.partition("=")
                stack[-1].attr[k] = v

        elif token.type in (T.T_ATTR_START, T.T_ATTR_END):
            continue

        elif token.type in (T.T_WHITESPACE, T.T_TEXT):
            # Extend existing text.
            cur = stack[-1].children
            if cur:
                if isinstance(cur[-1], Text):
                    cur[-1].value += token.value
                else:
                    cur.append(Text(token.value))
            else:
                # No leading whitespace on new strings.
                cur.append(Text(token.value.lstrip()))

        else:
            raise ParseException(f"Unknown token type: {token}")
    return stack[-1]
