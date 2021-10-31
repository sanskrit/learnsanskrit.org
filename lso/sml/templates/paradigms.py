from lso.sml.parse import Node, Text

from lso.sml.templates.base import View
from lso.sml.templates.sanskrit_text import DevanagariRoman


class NominalParadigm(View):
    def enter(self):
        return '<table class="paradigm">'

    def children(self):
        assert len(self.node.children) == 1
        text = self.node.children[0].value

        nodes = []

        def add_raw(s):
            nodes.append(Node("raw", [Text(s)]))

        add_raw("<tr><th>&nbsp;</th><th>Singular</th><th>Dual</th>")
        add_raw("<th>Plural</th></tr>")

        rows = text.strip().splitlines()
        for row in rows:
            case, s, d, p = row.split()
            add_raw(f"<tr><th>Case {case}</th>")
            for word in (s, d, p):
                if "-" in word and word != "-":
                    word, classes = word.split("-")
                else:
                    classes = None
                word = word.replace(",", ", ")

                if classes:
                    add_raw(f'<td class="{classes}">')
                else:
                    add_raw("<td>")
                if word == "_":
                    nodes.append(Text("&mdash;"))
                else:
                    nodes.append(DevanagariRoman.to_node(word))
                add_raw("</td>")
            add_raw("</tr>")

        return nodes

    def exit(self):
        return "</table>"


class VerbParadigm(View):
    def enter(self):
        return '<table class="paradigm">'

    def children(self):
        assert len(self.node.children) == 1
        text = self.node.children[0].value

        nodes = []

        def add_raw(s):
            nodes.append(Node("raw", [Text(s)]))

        add_raw("<tr><th>&nbsp;</th><th>Singular</th><th>Dual</th>")
        add_raw("<th>Plural</th></tr>")

        rows = text.strip().splitlines()
        names = ["3rd", "2nd", "1st"]
        for i, row in enumerate(rows):
            s, d, p = row.split()
            add_raw(f"<tr><th>{names[i]}</th>")
            for word in (s, d, p):
                if "," in word:
                    word = word.replace(",", ", ")
                if "-" in word:
                    word, classes = word.split("-")
                else:
                    classes = None

                if classes:
                    add_raw(f'<td class="{classes}">')
                else:
                    add_raw("<td>")

                nodes.append(DevanagariRoman.to_node(word))
                add_raw("</td>")
            add_raw("</tr>")

        return nodes

    def exit(self):
        return "</table>"
