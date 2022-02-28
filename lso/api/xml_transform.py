"""Transforms MW xml into HTML."""

from dataclasses import dataclass
from xml.etree import ElementTree as ET
from typing import Dict, Any, NamedTuple, Optional
from indic_transliteration import sanscript


class Rule(NamedTuple):
    tag: Optional[str]
    attrib: Dict[str, str] = {}
    text_before: str = ""
    text_after: str = ""


def text(before, after=""):
    return Rule(None, None, before, after)


transforms = {
    "lg": Rule("p", {"class": "verse"}),
    "l": Rule("span", {"class": "pada"}),
    "section": Rule("section", {}),
}

paren_rule = Rule("span", {"class": "paren"}, "(", ")")
bracket_rule = Rule("span", {"class": "paren"}, "[", "]")

# Tag meanings are documented here:
# https://www.sanskrit-lexicon.uni-koeln.de/talkMay2008/mwtags.html
mw_transforms = {
    # Root elements
    "H1": None,
    "H1A": None,
    "H1B": None,
    "H1E": None,
    "H2": None,
    "H2A": None,
    "H2B": None,
    "H3": None,
    "H3A": None,
    "H3B": None,
    "H4": None,
    "H4A": None,
    "H4B": None,
    # Record structure
    "h": None,
    "body": Rule("li", {"class": "mw-entry"}),
    "tail": None,
    # Head information -- hide all of it.
    "hc1": None,
    "hc3": None,
    "key1": None,
    "key2": None,
    # Body -- special characters
    "b": bracket_rule,
    "b1": bracket_rule,
    "p": paren_rule,
    "p1": paren_rule,
    "quote": Rule("q"),
    "sr": text("\u00b0"),
    "sr1": text("\u00b0"),
    "abE": None,
    "srs": text("*"),
    "srs1": text("*"),
    "shc": None,
    "shortlong": None,
    "auml": text("ä"),
    "euml": text("ë"),
    "ouml": text("ö"),
    "uuml": text("ü"),
    "etc": text("&c"),
    "etc1": text("&c"),
    "etcetc": text("&c"),
    "amp": text("&"),
    "eq": Rule("abbr", None, "="),
    "fs": text("/"),
    "msc": text(";"),
    "ccom": None,
    "ab": Rule("abbr"),
    "etym": Rule("i"),
    "s": Rule("span", {"lang": "sa"}, "##", "##"),
    "ns": Rule("span"),
    "s1": Rule("span"),
    "bio": Rule("b"),
    "bot": Rule("b"),
    "root": text("\u221a"),
    "ls": Rule("cite"),
    "lex": Rule("span", {"class": "lex"}),
    "vlex": Rule("span", {"class": "lex"}),
    "hom": None,
    "info": None,
    "lang": Rule("span"),
    # Also distinct tail pc, should be treated differently
    "pc": None,
    "pcol": Rule("span"),
    "cf": Rule("abbr", None, "cf."),
    "qv": Rule("abbr", None, "q.v."),
    "see": text(" see "),
    # Tail elements
    "L": None,
    "MW": None,
    "mul": None,
    "mat": None,
    "mscverb": None,
    # Not sure
    "div": Rule("br"),
}


def transform(xml_path: str) -> str:
    root = ET.parse(xml_path).getroot()

    for elem in root.iter():
        if elem.text:
            elem.text = sanscript.transliterate(elem.text, sanscript.HK, sanscript.IAST)

        rule = transforms[elem.tag]
        elem.tag = rule.tag
        elem.attrib = rule.attrib
    return ET.tostring(root, encoding="utf-8").decode("utf-8")


def transform_mw(blob: str) -> str:
    root = ET.fromstring(blob)

    for elem in root.iter():
        try:
            rule = mw_transforms[elem.tag]
        except KeyError:
            print(f"[xslt] unknown key {elem.tag}")
            continue
        if rule is None:
            elem.tag = elem.text = None
            continue

        elem.tag = rule.tag
        elem.attrib = rule.attrib or {}
        if elem.text:
            elem.text = rule.text_before + elem.text + rule.text_after

    untrans = ET.tostring(root, encoding="utf-8").decode("utf-8")
    return sanscript.transliterate("##" + untrans, sanscript.SLP1, sanscript.IAST)
