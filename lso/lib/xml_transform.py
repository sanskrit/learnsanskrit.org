"""
Lightweight XML transforms (instead of XSLT)
"""

from xml.etree import ElementTree as ET

class Rule(object):
    """A Rule defines a "translation" on a given element. It is not nearly as
    powerful as XSLT.

    :param tag: the new tag name
    :param attrib: the new attributes
    :param after_open: text to insert after the open tag
    :param before_close: text to insert before the close tag
    """
    def __init__(self, tag=None, attrib=None, after_open='', before_close=''):
        self.tag = tag
        self.attrib = attrib or {}
        self.after_open = after_open
        self.before_close = before_close


class TextRule(Rule):
    def __init__(self, after_open='', before_close=''):
        super(TextRule, self).__init__(after_open=after_open,
                                       before_close=before_close)


def translate(doc, rules):
    """Destructively transform `xml` according to the rules given. Since the
    structure of the XML element remains intact, this is less a transformation
    and more a translation.

    :param doc: an XML document, in text
    :param rules: a dict of that maps a tag name to a Rule
    """
    xml = ET.fromstring(doc)
    for elem in xml.getiterator():
        try:
            rule = rules[elem.tag]
            if rule is None:
                elem.tag = elem.text = elem.tail = None
        except KeyError:
            continue

        try:
            elem.tag = rule.tag
            elem.attrib = rule.attrib
            if rule.after_open:
                elem.text = rule.after_open + (elem.text or '')
            if rule.before_close:
                try:
                    last = elem[-1]
                    last.tail = (last.tail or '') + rule.before_close
                except IndexError:
                    elem.text = (elem.text or '') + rule.before_close
        except (AttributeError, TypeError):
            pass
    return ET.tostring(xml, 'utf-8').decode('utf-8')