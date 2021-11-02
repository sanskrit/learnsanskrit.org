from lso.sml.templates.sanskrit_text import *
from .common import *
from .paradigms import *
from .vyakarana import *


def wrap(start, end):
    """Convenience function for simple templates."""

    class Wrapped(View):
        def enter(self):
            return start

        def exit(self):
            return end

    return Wrapped


TEMPLATES = {
    "TEXT": TextView,
    "a": Anchor,
    "a-cite": AshtadhyayiRuleCitation,
    "aside": wrap('<aside class="true-aside">', "</aside>"),
    "br": wrap("<br>", ""),
    "cite": wrap("<cite>", "</cite>"),
    "code": wrap("<code>", "</code>"),
    "comm": Skip,
    "conjuncts": DevanagariConjuncts,
    "d": Devanagari,
    "dfn": wrap("<dfn>", "</dfn>"),
    "dhatu": Dhatupatha,
    "document": wrap("", ""),
    "em": wrap("<em>", "</em>"),
    "ex": Examples,
    "f5": wrap('<span class="f1">', "</span>"),
    "h": wrap("<h2>", "</h2>"),
    "hr": wrap("<hr>", ""),
    "i": Roman,
    "img": Image,
    "it": wrap("<i>", "</i>"),
    "topic": wrap("<i>", "</i>"),
    "lesson": LessonLink,
    "li": wrap("<li><p>", "</p></li>"),
    "nominal": NominalParadigm,
    "note": Note,
    "ol": wrap("<ol>", "</ol>"),
    "p": wrap("<p>", "</p>"),
    "prakriya": Prakriya,
    "raw": Raw,
    "rule": AshtadhyayiRule,
    "s": Sa2,
    "s-dfn": SanskritDefinition,
    "s-dr": DevanagariRoman,
    "s-td": SanskritTableCell,
    "s-tds": SanskritTableCellList,
    "sa-opt": SanskritOptionalDefinition,
    "sa1": Sa1,
    "sa2": Sa2,
    "sound-li": SoundListItem,
    "sounds-d": SoundsDevanagari,
    "sounds-dr": SoundsDevanagariRoman,
    "sounds-iast": SoundsIAST,
    "sounds-hk": SoundsHK,
    "sounds-iso": SoundsISO,
    "aka": wrap('<p class="aka f6">Also known as: ', "</p>"),
    "strong": wrap("<strong>", "</strong>"),
    "table": wrap('<table class="default">', "</table>"),
    "sandhi-table": wrap('<table class="sandhi">', "</table>"),
    "td": wrap("<td>", "</td>"),
    "th": wrap("<th>", "</th>"),
    "title": wrap("<h1>", "</h1>"),
    "todo": Todo,
    "tr": wrap("<tr>", "</tr>"),
    "two-col": wrap('<div class="df">', "</div>"),
    "ul": wrap("<ul>", "</ul>"),
    "url": FlaskRoute,
    "verb": VerbParadigm,
}
