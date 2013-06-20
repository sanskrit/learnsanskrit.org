# -*- coding: utf-8 -*-
"""
    lso.texts.lib
    ~~~~~~~~~~~~~

    XML processing for Sanskrit texts

    :license: MIT and BSD
"""

import re
import xml.etree.cElementTree as ET

from ..database import session
from .models import Text, Division, Segment, SegSegAssoc, Language, Author

XML_NS = '{http://www.w3.org/XML/1998/namespace}'
XML_ID = '{http://www.w3.org/XML/1998/namespace}id'
XML_LANG = '{http://www.w3.org/XML/1998/namespace}lang'


class Tag:

    """Various TEI tags"""

    TEI = 'TEI'
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

        self.lang_map = {x.slug: x.id for x in Language.query.all()}

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

        if tag == Tag.TEI:
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
        self.buf.append(data)

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
        """Handle the data in the TEI header.

        This function creates a :class:`Text` and a :class:`Division`
        for the current document if they don't exist already. Where
        possible, the function creates an :class:`Author` as well.

        """
        # Search for various data in teiHeader
        titleStmt_path = './fileDesc/titleStmt/'
        publicationStmt_path = './fileDesc/publicationStmt/'
        paths = {
            'name':  titleStmt_path + 'title',
            'author': titleStmt_path + 'author',
            'translator': titleStmt_path + 'editor[@role="translator"]',
            'slug':   publicationStmt_path + 'idno[@type="slug"]',
            'xmlid_prefix': publicationStmt_path + 'idno[@type="xml"]',
            'parent': publicationStmt_path + 'idno[@type="parent"]'
        }
        field_xml = {}
        field_text = {}
        for k in paths:
            try:
                elem = xml.find(paths[k])
                field_xml[k] = elem
                field_text[k] = elem.text
            except AttributeError:
                field_xml[k] = None
                field_text[k] = None

        # TEI document titles usually have some subtitle like
        # "[a machine readable transcription]". We should make sure to
        # get rid of that.
        name = field_text['name'].partition('[')[0].strip()
        slug = field_text['slug']
        xmlid_prefix = field_text['xmlid_prefix']

        # Two texts can have a parent-child relationship. This is
        # defined in the 'parent' field:
        parent = field_text['parent']
        if parent is None:
            parent_id = None
        else:
            parent = Text.query.filter(Text.xmlid_prefix == parent).first()
            if parent:
                parent_id = parent.id
            else:
                # TODO: notify user of invalid parent
                parent_id = None

        # `language_id` is used for both texts and authors
        language_id = self.lang_map[self.lang.split('-')[0]]

        # Create an :class:`Author` record as necessary.
        # Give precedence to translators: Kale's translation of the
        # Meghaduta is by Kale, not Kalidasa.
        author_xml = field_xml['translator'] or field_xml['author']
        if author_xml is not None:
            author_slug = author_xml.attrib[XML_ID]
            author = Author.query.filter(Author.slug == author_slug).first()
            if author:
                author_id = author.id
            else:
                author_name = self._text(author_xml)
                author = Author(name=author_name, slug=author_slug,
                                language_id=language_id)
                session.add(author)
                session.flush()
                author_id = author.id
        else:
            author_id = None

        div = Division(slug='', parent_id=None)
        self.division_map[''] = div
        session.add(div)
        session.flush()

        self.text = Text(
            name=name,
            slug=slug,
            xmlid_prefix=xmlid_prefix,
            language_id=language_id,
            author_id=author_id,
            parent_id=parent_id,
            division_id=div.id)
        session.add(self.text)
        session.flush()

    def _text(self, elem):
        """Return the plain text in a given Element.

        If the element has no children, this is nearly the same as
        running `elem.text`. Leading and trailing whitespace are
        stripped out.

        :param elem: the element to process"""

        return re.sub('<[^<]+?>', '', ET.tostring(elem)).strip()

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
            parent_id = self.text.parent_id
            other = Segment.query.filter(Segment.text_id == parent_id)\
                                 .filter(Segment.slug == path).first()
            if other is not None:
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
        attr = elem.attrib
        html_attr = {}

        if tag == 'l':
            if attr.get('rend') == 'indent':
                elem.tag = 'span'
                html_attr['class'] = 'indent'
            else:
                elem.tag = None
            elem.append(ET.Element('br'))
        elif tag == 'lg':
            elem.tag = 'p'
        elif elem.tag == 'hi':
            if attr['rend'] == 'italic':
                elem.tag = 'i'

        elem.attrib = html_attr

    # Delete <wrap>
    xml.tag = None
    return ET.tostring(xml)


def main():
    import sys
    process_text_xml(sys.argv[1])


if __name__ == '__main__':
    main()
