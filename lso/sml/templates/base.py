import re
from typing import Any, Dict, List

from lso.sml.parse import Node


class View(object):
    def __init__(self, node: Node, ctx: Dict[str, Any] = None):
        self.node = node

    def enter(self) -> str:
        return ""

    def children(self) -> List[Node]:
        return self.node.children

    def exit(self) -> str:
        return ""


class TextView(View):
    @staticmethod
    def cleanup(s: str) -> str:
        s = s.replace("--", "&mdash;")
        s = s.replace(' "', " &ldquo;")
        s = re.sub(r'([ (])"', r"\1&ldquo;", s)
        s = re.sub(r'"([ )])', r"&rdquo;\1", s)
        s = re.sub(r'^"', r"&ldquo;", s)
        s = re.sub(r'\n"', r" &ldquo;", s)
        s = re.sub(r'"', r"&rdquo;", s)
        return s

    def enter(self):
        assert not self.node.children, "TEXT node shouldn't have children."
        return self.cleanup(self.node.value)
