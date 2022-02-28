import re
from typing import List, Dict

import lso.sml.parse as parser
from lso.sml.parse import Node, Text

from lso.sml.templates import View, TextView
from lso.sml.templates import TEMPLATES


class Missing(View):

    """Template for nodes that can't be understood."""

    def enter(self):
        return '<span style="background: #f00;">' + self.node.name

    def exit(self):
        return "</span>"


# Block elements aren't treated as paragraphs.
BLOCK_ELEMS = {"ul", "ol", "li", "h", "title", "note", "aside"}
BLOCK_WRAPPERS = {"note", "aside"}


def split_paragraphs(node: Node):
    """Preprocess and split into paras"""
    node_chunks = []
    buf = []
    for child in node.children:
        # Split on double line break in text
        if child.name == "TEXT":
            chunks = re.split(r"(\s*\n\s*\n\s*)", child.value)
            for i, chunk in enumerate(chunks):
                # Double line break
                if i % 2 == 1:
                    node_chunks.append(buf)
                    buf = []
                elif chunk.strip():
                    buf.append(Text(chunk))
        else:
            if child.name in BLOCK_WRAPPERS:
                split_paragraphs(child)
            buf.append(child)
    if buf:
        node_chunks.append(buf)

    new_children = []
    for chunk in node_chunks:
        if chunk[0].name in BLOCK_ELEMS:
            new_children.extend(chunk)
        else:
            new_children.append(Node("p", chunk))
    node.children = new_children


def render_buf(node: Node, ctx, templates) -> List[str]:
    buf = []
    t = templates.get(node.name, Missing)(node, ctx)

    buf.append(t.enter())
    for child in t.children():
        buf.extend(render_buf(child, ctx, templates))
    buf.append(t.exit())

    return buf


def render(raw: str, ctx=None) -> Dict[str, str]:
    tree = parser.parse(raw)
    split_paragraphs(tree)
    buf = render_buf(tree, ctx or {}, TEMPLATES)
    content = "".join(buf)

    title = "(missing)"
    for c in tree.children:
        # Extract title
        if c.name == "title":
            buf = []
            for child in c.children:
                buf.extend(render_buf(child, ctx, TEMPLATES))
            title = "".join(buf)

    return {"title": title, "content": content}


def render_inline(raw: str, ctx=None) -> str:
    tree = parser.parse(raw)
    buf = render_buf(tree, ctx or {}, TEMPLATES)
    content = "".join(buf)
    return content
