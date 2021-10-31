import lso.sml.render as render_sml
from markupsafe import Markup
from indic_transliteration import sanscript


def sml(s: str) -> str:
    return Markup(render_sml.render_inline(s))


def devanagari(s: str) -> str:
    return sanscript.transliterate(s, "hk", "devanagari")


def roman(s: str) -> str:
    return sanscript.transliterate(s, "hk", "iast")


def sa2(s: str) -> str:
    t = roman(s)
    return Markup(f'<span lang="sa" class="sa2">{t}</span>')


def transliterate_generic(s: str, result: str) -> str:
    return sanscript.transliterate(s, "hk", result)
