from lso import sanscript
from lso.sml.parse import Node, Text
from lso.sml.templates.base import View


class Devanagari(View):
    """Devanagari text."""

    @staticmethod
    def to_node(text):
        return Node("d", [Text(text)])

    def enter(self):
        # No sa1 or sa2 -- always devanagari
        return '<span lang="sa" class="dev">'

    def children(self):
        for child in self.node.children:
            if child.name == "TEXT":
                text = child.value
                text = sanscript.transliterate(text, "hk", "devanagari")
                child.value = text
        return self.node.children

    def exit(self):
        return "</span>"


class Roman(View):
    """Romanized text."""

    @staticmethod
    def to_node(text):
        return Node("i", [Text(text)])

    def enter(self):
        # No sa1 or sa2 -- always roman
        return '<span lang="sa" class="iast">'

    def children(self):
        for child in self.node.children:
            if child.name == "TEXT":
                text = child.value
                text = sanscript.transliterate(text, "hk", "iast")
                child.value = text
        return self.node.children

    def exit(self):
        return "</span>"


class Roman(View):
    """Romanized text."""

    @staticmethod
    def to_node(text):
        return Node("i", [Text(text)])

    def enter(self):
        # No sa1 or sa2 -- always roman
        return '<span lang="sa" class="iast">'

    def children(self):
        for child in self.node.children:
            if child.name == "TEXT":
                text = child.value
                text = sanscript.transliterate(text, "hk", "iast")
                child.value = text
        return self.node.children

    def exit(self):
        return "</span>"


class Sa1(Devanagari):
    """Devanagari text that can be transliterated."""

    @staticmethod
    def to_node(text):
        return Node("sa1", [Text(text)])

    def enter(self):
        return '<span lang="sa" class="sa1">'


class Sa2(Roman):
    """Romanized text that can be transliterated."""

    @staticmethod
    def to_node(text):
        return Node("sa2", [Text(text)])

    def enter(self):
        return '<span lang="sa" class="sa2">'


class DevanagariRoman(View):
    @staticmethod
    def to_node(text):
        return Node("s-dr", [Text(text)])

    def children(self):
        assert len(self.node.children) == 1
        text = self.node.children[0].value.strip()
        return [
            Sa1.to_node(text),
            Node("br"),
            Sa2.to_node(text),
        ]
