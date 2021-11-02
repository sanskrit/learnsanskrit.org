import re
from typing import Any, Dict, List

from lso import consts
from lso import paradigms
from lso import sanscript
from lso.sml.parse import Node, Text

from flask import url_for

from lso.sml.templates.base import View
from lso.sml.templates import Devanagari, Sa1, Sa2
from lso.sml.templates.sanskrit_text import DevanagariRoman
from lso.sml.templates.utils import split_multiline_text


def quick_sa(raw_text: str) -> List[Node]:
    tokens = re.split(r"(`[a-zA-Z~_-]+)", raw_text)
    nodes = []
    for t in tokens:
        if t.startswith("`"):
            # Separate English plural s
            t_sa, _, gap = t.partition("_")
            nodes.append(Sa2.to_node(t_sa[1:]))
            nodes.append(Text(gap))
        else:
            nodes.append(Text(t))
    return nodes

    def exit(self) -> str:
        return ""


class Examples(View):
    def enter(self):
        return '<ul class="examples">'

    def children(self):
        assert len(self.node.children) == 1
        text = self.node.children[0].value
        text = text.replace(">", "→")

        children = []
        examples = split_multiline_text(text)
        for ex in examples:
            if not ex.strip():
                continue
            ex = ex.replace("[", "<mark>").replace("]", "</mark>")
            lines = ex.splitlines()
            assert 1 <= len(lines), lines

            sa = lines[0]
            li_nodes = [
                Sa1.to_node(sa.replace(".", "|")),
                Node("br"),
                Sa2.to_node(sa.replace("..", ".")),
            ]
            try:
                en = lines[1]
                li_nodes.extend([Node("br")])
                li_nodes.extend(quick_sa(en))
            except IndexError:
                pass
            try:
                note = " ".join(lines[2:])
                li_nodes.extend([Node("br")])
                li_nodes.extend(quick_sa(note))
            except IndexError:
                pass

            children.append(Node("li", li_nodes))

        return children

    def exit(self):
        return "</ul>"


class Note(View):
    def enter(self):
        return '<aside class="note"><p>'

    def exit(self):
        return "</p></aside>"


class Anchor(View):
    def enter(self):
        href = self.node.attr["href"]
        return f'<a href="{href}" target="_blank">'

    def exit(self):
        return "</a>"


class SanskritOptionalDefinition(View):
    def enter(self):
        # HACK no starting space
        return " ("

    def children(self):
        assert len(self.node.children) == 1
        text = self.node.children[0].value
        sa, _, en = text.partition(" ")
        sa = Node("s-dfn", [Text(sa)])
        if en:
            en = Text(en)
            return [sa, Text(", "), en]
        else:
            return [sa]

    def exit(self):
        return ")"


class SanskritDefinition(View):
    def enter(self):
        return "<dfn>"

    def children(self):
        assert len(self.node.children) == 1
        text = self.node.children[0].value
        return [Sa2.to_node(text)]

    def exit(self):
        return "</dfn>"


class SanskritTableCell(SanskritDefinition):
    @staticmethod
    def to_node(s):
        return Node("s-td", [Text(s)])

    def enter(self):
        return "<td>"

    def exit(self):
        return "</td>"


class SanskritTableCellList(View):
    def children(self):
        assert len(self.node.children) == 1
        text = self.node.children[0].value

        ret = []
        for td in text.split("|"):
            td = td.strip()
            ret.append(SanskritTableCell.to_node(td))
        return ret


class SoundsView(View):
    def enter(self):
        return f'<ul class="sounds">'

    @property
    def entries(self):
        assert len(self.node.children) == 1
        data = self.node.children[0].value
        return data.split()

    def exit(self):
        return "</ul>"


class SoundsDevanagariRoman(SoundsView):
    def children(self):
        children = []
        for entry in self.entries:
            sound, _, color = entry.partition("-")
            children.append(
                Node(
                    "sound-li",
                    [
                        DevanagariRoman.to_node(sound),
                    ],
                    **{"class": f"sth-{color}"},
                )
            )
        return children


class SoundsDevanagari(SoundsView):
    def children(self):
        children = []
        for entry in self.entries:
            sound, _, color = entry.partition("-")
            children.append(
                Node(
                    "sound-li",
                    [
                        Sa1.to_node(sound),
                    ],
                    **{"class": f"sth-{color}"},
                )
            )
        return children


class SoundsIAST(SoundsView):
    def children(self):
        children = []
        for entry in self.entries:
            sound, _, color = entry.partition("-")
            children.append(
                Node(
                    "sound-li",
                    [
                        Raw.to_node('<span class="f4">'),
                        Node("i", [Text(sound)]),
                        Raw.to_node("</span>"),
                    ],
                    **{"class": f"sth-{color}"},
                )
            )
        return children


class SoundsHK(SoundsView):
    def children(self):
        children = []
        for entry in self.entries:
            sound, _, color = entry.partition("-")
            # Workaround for my hack
            hk = sound.replace("LL", "lRR").replace("L", "lR")
            children.append(
                Node(
                    "sound-li",
                    [
                        Raw.to_node('<span class="f4">'),
                        Node("i", [Text(sound)]),
                        Raw.to_node("</span>"),
                        Node("br"),
                        Node("code", [Text(hk)]),
                    ],
                    **{"class": f"sth-{color}"},
                )
            )
        return children


class SoundsISO(SoundsView):
    def enter(self):
        return f'<ul class="sounds sa-iso">'

    def children(self):
        children = []
        for entry in self.entries:
            sound, _, color = entry.partition("-")
            text = sanscript.transliterate(sound, "hk", "kolkata")
            children.append(
                Node(
                    "sound-li",
                    [
                        Raw.to_node('<span class="f4">'),
                        Raw.to_node(text),
                        Raw.to_node("</span>"),
                    ],
                    **{"class": f"sth-{color}"},
                )
            )
        return children


class DevanagariConjuncts(SoundsView):
    def children(self):
        children = []
        for sound in self.entries:
            children.append(
                Node(
                    "sound-li",
                    [
                        DevanagariRoman.to_node(sound),
                    ],
                )
            )
        return children


class SoundListItem(View):
    def enter(self):
        cls = self.node.attr.get("class")
        if cls:
            return f'<li class="{cls}">'
        else:
            return "<li>"

    def exit(self):
        return "</li>"


class FlaskRoute(View):
    def enter(self):
        args = dict(self.node.attr)
        route = args.pop("r")
        url = url_for(route, **args)
        return f'<a href="{url}">'

    def exit(self):
        return "</a>"


class LessonLink(View):
    def enter(self):
        args = dict(self.node.attr)
        route = args.pop("r")
        topic, slug = route.strip().split("/")
        url = url_for("guide.lesson", topic=topic, slug=slug)
        return f'<a href="{url}">'

    def exit(self):
        return "</a>"


class Skip(View):
    def children(self):
        return []


class Image(View):
    def enter(self):
        url = url_for("static", filename="img/" + self.node.attr["src"])
        return f'<img src="{url}">'


class Raw(View):
    @staticmethod
    def to_node(text: str):
        return Node("raw", [Text(text)])

    def enter(self):
        assert len(self.node.children) == 1
        return self.node.children[0].value

    def children(self):
        return []


class Todo(View):
    def enter(self):
        url = consts.MAILING_LIST_URL
        return (
            '<aside class="note">'
            "<p>This content is still being developed. Please check back later."
            " You can subscribe to updates on our "
            f'<a href="{url}" target=_blank>'
            "mailing list.</a></p>"
            "</aside>"
        )
