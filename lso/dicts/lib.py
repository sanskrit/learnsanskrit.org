  #!/usr/bin/python
  # -*- encoding: utf-8 -*-

import re
import xml.etree.ElementTree as ET
from sanskrit.letters import sanscript as S

from lso.lib.xml_transform import Rule, TextRule, translate

paren_rule = Rule('span', {'class': 'paren'}, '(', ')')

mw = {
    'ab': Rule('abbr'),                       # abbreviation
    'abE': None,                              # English abbr. superscript
    'amp': TextRule('&'),                     # ampersand
    'AND': None,                              # (for multiple head words)
    'as0': None,                              # MW anglicized (AS)
    'as1': Rule('span', {'class': 'ref'}),    # MW anglicized (SLP1)
    'asp0': None,                             # MW anglicized (AS, plural)
    'auml': TextRule(u'ä'),                   # 'a' umlaut
    'b': TextRule('[', ']'),                  # brackets
    'b1': TextRule('[', ']'),                 # brackets
    'bio': Rule('b'),                         # taxonomy (animal)
    'body': Rule('p'),                        # definition wrapper
    'bot': Rule('b'),                         # taxonomy (plant)
    'c': Rule(None),                          # text chunk
    'c1': Rule(None),                         # text chunk
    'c2': Rule(None),                         # text chunk
    'c3': Rule(None),                         # text chunk
    'cf': TextRule('cf.'),                    # "cf."
    'dL': None,                               # link to daughter record
    'eq': Rule('abbr', None, '='),            # "equals"
    'etc': TextRule('&c'),                    # "etc."
    'etc1': TextRule('&c'),                   # "etc."
    'etcetc': TextRule('&c'),                 # "etc."
    'etym': TextRule('i',),                   # (Skt.?) etymology
    'euml': TextRule(u'ë'),                   # 'e' umlaut
    'fcom': TextRule(u'°'),                   # "Rare; significance unclear"
    'fs': TextRule('/'),                      # separates entry senses
    'gk': Rule('b'),                          # Greek
    'lex': Rule('span', {'class': 'lex'}),    # lexical info
    'ls': Rule('cite'),                       # textual citation
    'msc': TextRule(';'),                     # separates verb senses
    'ouml': TextRule(u'ö'),                   # 'o' umlaut
    'OR': None,                               # (for multiple head words)
    'p': paren_rule,                          # parentheses
    'p1': paren_rule,                         # parentheses
    'pc': None,                               # intratextual reference
    'pcol': None,                             # intratextual reference
    'phw': Rule(None),                        # implicit head word
    'p1': paren_rule,                         # parentheses
    'pL': None,                               # Link to parent record
    'quote': Rule('q'),                       # quoted text
    'qv': Rule('abbr', None, 'q.v.'),         # "q.v."
    'root': TextRule(u'√'),                   # verb root
    's': Rule('span', {'class': 'sa2'}, '##', '##'),  # Sanskrit
    'see': TextRule(' see '),                         # "see"
    'shc': None,                              # (variable length vowel)
    'shortlong': None,                        # (variable length vowel)
    'sr':  TextRule(u'°'),                    # an elided word
    'sr1': TextRule(u'°'),                    # an elided word
    'srs': TextRule(u'*'),                    # sandhied vowel (non-vrddhi)
    'srs1': TextRule(u'*'),                   # sandhied vowel (vrddhi)
    'to': None,                               # infinitive marker
    'usage': Rule(None),                      # experimental
    'uuml': TextRule(u'ü'),                   # 'u' umlaut
    'vlex': Rule('span', {'class': 'vlex'}),  # lexical category
}

def mw_transform(data, to_script):
    clean_data = re.sub('[~_]', ' ', data)
    clean_data = re.sub(' ([,;])', '\\1', clean_data)
    result = translate(clean_data, mw)
    return S.transliterate('##' + result, S.SLP1, to_script)
