# -*- coding: utf-8 -*-
"""
    lso.texts.lib
    ~~~~~~~~~~~~~

    XML processing for Sanskrit texts

    :license: MIT and BSD
"""

import xml.etree.cElementTree as ET

from ..database import session
from .models import Text, Division, Segment, SegSegAssoc

XML_NS = '{http://www.w3.org/XML/1998/namespace}'
XML_ID = '{http://www.w3.org/XML/1998/namespace}id'
XML_LANG = '{http://www.w3.org/XML/1998/namespace}lang'


class Tag:
    TEI_HEADER = 'teiHeader'
    TEXT = 'text'
    ANCHOR = 'anchor'
    IDNO_TAG = 'idno'
    CHOICE = 'choice'
    SEG = 'seg'
    WORD = 'w'
    MORPHEME = 'm'
    DIV = 'div'
    DESC = 'desc'
    LG = 'lg'
    P = 'p'
    SEGMENT_TAGS = (DIV, P, LG)


class DocumentTarget:

    """Helper class for stream-parsing XML documents"""

    def __init__(self):
        # Stores iterated data
        self.buf = []
        # First tag of the current block
        self.block_tag = None
        # depth level in the current block. `0` is the top level.
        self.depth = 0

        # Reference to the :class:`Text` record
        self.text = None
        # Document language
        self.lang = None
        # Maps prefix strings to textual divisions
        self.division_map = {}
        #
        self.position = 1

    # XML parser events
    # -----------------
    def start(self, tag, attrib):
        b = self.buf

        is_tei_header = tag == Tag.TEI_HEADER
        is_segment = tag in Tag.SEGMENT_TAGS and XML_ID in attrib

        # a) new block
        if is_tei_header or is_segment:
            del b[:]
            self.block_tag = tag
            self.depth = 0

        # b) deeper in current block
        elif self.block_tag:
            self.depth += 1

        if tag == Tag.TEXT:
            self.lang = attrib.get(XML_LANG, None)

        # Inside a block
        if self.block_tag:
            attr_data = []
            for k, v in attrib.items():
                # Replace xml namespace with 'xml:'
                pre, cur, post = k.partition(XML_NS)
                if cur:
                    k = 'xml:' + post

                # add to attr buffer
                attr_data.append('%s="%s"' % (k, v))

            attr_string = ' '.join(attr_data)
            if attr_string:
                b.append('<%s %s>' % (tag, attr_string))
            else:
                b.append('<%s>' % tag)

    def data(self, data):
        self.buf.append(data.strip())

    def end(self, tag):
        b = self.buf
        b.append('</%s>' % tag)

        if tag == self.block_tag and not self.depth:
            self.handle(''.join(b))
            self.block_tag = None
            del b[:]
        else:
            self.depth -= 1

    def close(self):
        session.commit()
        session.close()
        del self.buf[:]

    # Data handlers
    # -------------
    def handle(self, blob):
        xml = ET.fromstring(blob.replace('&', '&amp;').encode('utf-8'))
        if xml.tag in Tag.SEGMENT_TAGS:
            self.handle_segment(blob, xml)
        elif xml.tag == Tag.TEI_HEADER:
            self.handle_tei_header(blob, xml)

    def handle_tei_header(self, blob, xml):
        # Query for data from teiHeader
        titleStmt_path = './fileDesc/titleStmt/'
        publicationStmt_path = './fileDesc/publicationStmt/'
        paths = {
            'name':  titleStmt_path + 'title',
            'author': titleStmt_path + 'author',
            'slug':   publicationStmt_path + 'idno[@type="slug"]',
            'xmlid_prefix': publicationStmt_path + 'idno[@type="xml"]',
            'parent': publicationStmt_path + 'idno[@type="parent"]'
        }
        fields = {}
        for k in paths:
            try:
                fields[k] = xml.find(paths[k]).text
            except AttributeError:
                fields[k] = None

        # Preprocess
        name = fields['name'].partition('[')[0].strip()
        slug = fields['slug']
        xmlid_prefix = fields['xmlid_prefix']
        parent = fields['parent']
        if parent is None:
            parent_id = None
        else:
            parent = Text.query.filter(Text.xmlid_prefix == parent).one()
            parent_id = parent.id

        div = Division(slug='', parent_id=None)
        self.division_map[''] = div
        session.add(div)
        session.flush()

        self.text = Text(
            name=name,
            slug=slug,
            xmlid_prefix=xmlid_prefix,
            language_id=None,
            parent_id=parent_id,
            division_id=div.id)
        session.add(self.text)
        session.flush()

    def _create_divs(self, slug):
        div_slug, dot, _ = slug.rpartition('.')
        try:
            return self.division_map[div_slug]
        except KeyError:
            if dot:
                parent = self._create_divs(div_slug)
                d = Division(slug=div_slug, parent_id=parent.id)
                self.division_map[div_slug] = d
                session.add(d)
                session.flush()
                return d
            else:
                return self.division_map['']

    def handle_segment(self, blob, xml):
        attr = xml.attrib

        # Create divisions as necessary
        slug = attr[XML_ID]
        _, _, slug = slug.partition('.')
        div = self._create_divs(slug)

        s = Segment(
            slug=slug,
            content=blob,
            position=self.position,
            text_id=self.text.id,
            division_id=div.id)

        corresp = attr.get('corresp', None)
        if corresp:
            corresp = corresp.replace('#', '')
            text, _, path = corresp.partition('.')
            other = Segment.query.filter(Segment.text_id == self.text.parent_id)\
                                 .filter(Segment.slug == path).first()
            s.parent_assocs.append(SegSegAssoc(parent=other,
                                               child=s,
                                               text=self.text))

        session.add(s)
        session.flush()
        self.position += 1


def process_text_xml(path):
    """
    Parse the given file and map it to the database.

    :param filename: path to the text file
    """

    with open(path) as f:
        parser = ET.XMLParser(target=DocumentTarget())
        for line in f:
            parser.feed(line)
        parser.close()


def transform(data):
    wrapped_data = '<wrap>%s</wrap>' % data
    xml = ET.fromstring(wrapped_data.encode('utf-8'))
    for elem in xml.iter():
        tag = elem.tag

        if tag == 'l':
            elem.tag = None
            elem.append(ET.Element('br'))
        elif tag == 'lg':
            elem.tag = 'p'
            elem.attrib = {}

    # Delete <wrap>
    xml.tag = None
    return ET.tostring(xml)


def main():
    import sys
    process_text_xml(sys.argv[1])


if __name__ == '__main__':
    main()
