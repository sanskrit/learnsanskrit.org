from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.util import etree

from sanskrit import sanscript

class SanskritPattern(Pattern):
    def handleMatch(self, match):
        attrib = {'lang': 'sa', 'class': 'sa2'}
        el = etree.Element('span', **attrib)
        text = match.group(2)
        devanagari = sanscript.transliterate(text, 'hk', 'iast')
        el.text = devanagari
        return el


class SanskritExtension(Extension):
    """Modify backticks (`) to transliterate to Devanagari."""

    def extendMarkdown(self, md, md_globals):
        sp = SanskritPattern(r'\`([^`]+)\`')
        md.inlinePatterns.add('sanskrit', sp, '<backtick')
