from flask import (Blueprint, flash, redirect, render_template, url_for,
                   jsonify)
from sqlalchemy import and_

import lib as L
from lso.views import api
from .models import (Author, Category, Language, Segment,
                     SegSegAssoc as SSA, Text)

# Maps slugs to IDs
LANGUAGES = None
# Maps IDs to slugs
CATEGORIES = None
# Standard size of a segment page
PAGE_SIZE = 1
# Minimum size for a segment page
MIN_PAGE_SIZE = 1


class Card:

    """A segment with its associated children. The metaphor here is that this
    is like an index card, i.e. a discrete unit of content.

    I used my own class because Flask makes namedtuple JSON serialization hard
    to modify.
    """

    def __init__(self, primary, translations, commentaries):
        self.primary = primary
        self.translations = translations
        self.commentaries = commentaries


class ChildCard:

    """A child texts with associated segments.

    I used my own class because Flask makes namedtuple JSON serialization hard
    to modify.
    """

    def __init__(self, text_id, segments):
        self.text_id = text_id
        self.segments = segments


# No URL prefix; this has '/texts' and '/authors'.
bp = Blueprint('texts', __name__, static_folder='static',
               template_folder='templates')


def view_setup():
    bp.before_app_first_request(load_data)


def load_data():
    """Load some simple data from the database."""
    global CATEGORIES, LANGUAGES
    CATEGORIES = {x.id: x.slug for x in Category.query.all()}
    LANGUAGES = {x.slug: x.id for x in Language.query.all()}


@bp.context_processor
def inject_helpers():
    return {
        'categorize_texts': categorize_texts,
        'xml_transform': L.transform
    }


# Helper functions
# ~~~~~~~~~~~~~~~~

def _flash_missing_text(slug):
    flash("We can't find text \"%s\" in the collection." % slug)


def paginate(items, size, min_size=0):
    """Return a list of items grouped into pages.

    :param size: the page size
    :param min_size: the mininum page size. If a page is smaller than
                     `min_size`, then it is merged into the previous
                     page, if one exists.
    """
    pages = []
    for start in xrange(0, len(items), size):
        pages.append(items[start:start + size])

    try:
        if len(pages[-1]) < min_size:
            pages[-2].extend(pages[-1])
            pages.pop()
    except IndexError:
        pass
    return pages


def paginate_division(division, size, min_size):
    last_slug = division.segments[-1].slug.rpartition('.')[2]
    number = int(last_slug)
    slugs = ['%s.%s' % (division.slug, n) for n in range(1, number + 1)]
    return paginate(slugs, size, min_size)


def peer_divisions(text, cur):
    """Get divisions with the same depth as `cur`.

    :param `cur`: a :class:`Division`.
    """
    divs = text.division.mp.query_descendants().all()
    return [d for d in divs if d.mp_depth == cur.mp_depth]


def page_to_query_string(page):
    """Convert a page to a query string.

    :param page: a list of items
    """
    p1, p2 = page[0], page[-1]
    if p1 == p2:
        return {'query': p1, 'readable': p1}
    else:
        return {'query': '-'.join((p1, p2)), 'readable': ' - '.join((p1, p2))}


def categorize_texts(texts):
    """Sort a list of texts into categories.

    :param texts: a list of :class:`Text` objects.
    """
    data = defaultdict(list)
    for text in texts:
        key = CATEGORIES[text.category_id]
        data[key].append(text)
    return data


# Data helpers
# ~~~~~~~~~~~~

def make_cards(child_texts, parent_segments):
    """Make cards by combining parent and child segments.

    :param child_texts: Child texts
    :param parent_segments: Parent segments
    :return: a list of `Card`s.
    """
    parent_segment_ids = {x.id : x for x in parent_segments}
    child_text_ids = [x.id for x in child_texts]
    results = SSA.query.filter(SSA.parent_id.in_(parent_segment_ids))\
                       .filter(SSA.text_id.in_(child_text_ids)).all()

    # Map from (parent segment, text) to a list of segments.
    join = {}
    for r in results:
        # TODO: don't query for each child.
        key = (r.parent_id, r.child.text_id)
        join.setdefault(key, []).append(r.child)

    cards = []
    for s in parent_segments:
        translations = []
        commentaries = []
        for t in child_texts:
            child_card = ChildCard(text_id=t.id, segments=join.get((s.id, t.id), []))
            if CATEGORIES[t.category_id] == 'translation':
                translations.append(child_card)
            elif CATEGORIES[t.category_id] == 'commentary':
                commentaries.append(child_card)
            else:
                raise
        cards.append(Card(primary=s,
                          translations=translations,
                          commentaries=commentaries))
    return cards


def get_segments_for_text_and_query(text_id, query_groups):
    """Get all segments in `text_id` that match `query_groups`.

    :param text_id: the ID of the text
    :param query_groups: a list of queries
    """
    base_query = Segment.query.filter(Segment.text_id == text_id)\
                        .order_by(Segment.position.asc())
    for group in query_groups:
        pre, _, post = group.partition('-')
        if pre and post:
            results = base_query.filter(Segment.slug.in_([pre, post])).all()
            try:
                first, last = results
                middle = base_query.filter(and_(
                    Segment.position > first.position,
                    Segment.position < last.position)).all()
                return [first] + middle + [last]
            # Only one result could be unpacked -> keep just the first
            # TODO: return more than one result here.
            except ValueError:
                if results:
                    return [results[0]]
        else:
            return [base_query.filter(Segment.slug == pre).first()]


def find_prev_and_next(query_groups, primary_segments, text):
    if len(query_groups) == 1:
        first, last = primary_segments[0], primary_segments[-1]

        cur = first.division
        cur_pages = paginate_division(cur, PAGE_SIZE, MIN_PAGE_SIZE)
        divs = None

        slug_index_map = {slug: (i, j) for i, page in enumerate(cur_pages)
                          for j, slug in enumerate(page)}

        # prev
        i, j = slug_index_map[first.slug]
        # prev in current division
        if i:
            prev = cur_pages[i - 1]
            if j:
                prev.extend(cur_pages[i][:j])
        # prev in previous division
        else:
            divs = divs or peer_divisions(text, cur)
            for k, d in enumerate(divs):
                if d.id == cur.id:
                    break
            if k:
                pages = paginate_division(
                    divs[k - 1], PAGE_SIZE, MIN_PAGE_SIZE)
                prev = pages[-1]
            else:
                prev = None

        # next
        i, j = slug_index_map[last.slug]
        next = cur_pages[i][j + 1:]
        # next in current division
        try:
            if len(next) < MIN_PAGE_SIZE:
                next.extend(cur_pages[i + 1])
        except IndexError:
            pass
        # next in next division
        if not next:
            divs = divs or peer_divisions(text, cur)
            for k, d in enumerate(divs):
                if d.id == cur.id:
                    break
            try:
                pages = paginate_division(
                    divs[k + 1], PAGE_SIZE, MIN_PAGE_SIZE)
                next = pages[0]
            except IndexError:
                next = None

        # convert to query form
        if prev:
            prev = page_to_query_string(prev)
        if next:
            next = page_to_query_string(next)
    else:
        prev = next = None

    return prev, next


def segments_data(text, slug, query, child_slugs):
    """
    :param text:
    :param slug:
    :param query:
    :param related:
    """
    query_groups = query.split(',')
    primary_segments = get_segments_for_text_and_query(text.id, query_groups)

    if child_slugs:
        child_texts = Text.query.filter(Text.slug.in_(child_slugs)).all()
        active_children = [t.id for t in child_texts]
    else:
        child_texts = []
        active_children = []

    cards = make_cards(child_texts, primary_segments)

    prev, next = find_prev_and_next(query_groups, primary_segments, text)

    readable_range = query.replace('-', ' - ').replace(',', ', ')
    readable_query = '%s %s' % (text.name, readable_range)

    secondary_texts = {t.id: t for t in text.children}
    all_translations = [t.id for t in text.children
                        if CATEGORIES[t.category_id] == 'translation']
    all_commentaries = [t.id for t in text.children
                        if CATEGORIES[t.category_id] == 'commentary']

    return dict(
        text=text,
        query=query,
        readable_query=readable_query,
        cards=cards,
        active_children=active_children,
        all_translations=all_translations,
        all_commentaries=all_commentaries,
        secondary_texts=secondary_texts,
        prev=prev,
        next=next,
        related=child_slugs
    )


# Author endpoints
# ~~~~~~~~~~~~~~~~

@bp.route('/authors/')
def author_index():
    authors = Author.query.all()
    sanskrit = []
    english = []
    for a in authors:
        if a.language_id == LANGUAGES['sa']:
            sanskrit.append(a)
        else:
            english.append(a)
    return render_template('/texts/author_index.html', sanskrit=sanskrit,
                           english=english)


@bp.route('/authors/<slug>')
def author(slug):
    author = Author.query.filter(Author.slug == slug).first()
    return render_template('texts/author.html', author=author)


# Text/segment endpoints
# ~~~~~~~~~~~~~~~~~~~~~~

@bp.route('/texts/')
def index():
    """A basic index page containing all texts in the collection."""

    texts = Text.query.filter(Text.language_id == LANGUAGES['sa'])\
                      .filter(Text.parent_id == None)\
                      .all()
    return render_template('texts/index.html', texts=texts)


@bp.route('/texts/<slug>/')
def text(slug):
    """The main page of a given text.

    :param slug: the text's slug
    """
    text = Text.query.filter(Text.slug == slug).first()
    if text is None:
        _flash_missing_text(slug)
        return redirect(url_for('.index'))

    divisions = text.division.mp.query_descendants().all()
    divisions = [d for d in divisions if d.segments]
    pages = []
    for d in divisions:
        division_pages = paginate_division(d, PAGE_SIZE, min_size=MIN_PAGE_SIZE)
        page_queries = map(page_to_query_string, division_pages)
        pages.append(page_queries)

    return render_template('texts/text.html', text=text,
                           divs=divisions,
                           pages=pages)


@bp.route('/texts/<slug>/<query>')
@bp.route('/texts/<slug>/<query>+<list:related>')
def segment(slug, query, related=None):
    """Query a given text for a group of segments. If related texts are
    listed too, show their corresponding segments.

    :param slug: the text's slug
    :param query: the segment query to perform. This is a CSL of slug
                  groups, e.g. '1.2', '1.1-1.5', and so on.
    :param related: if specified, a CSL of the slugs of related texts.
    """

    primary_text = Text.query.filter(Text.slug == slug).first()
    if primary_text is None:
        _flash_missing_text(slug)
        return redirect(url_for('.index'))

    # Data
    data = segments_data(primary_text, slug, query, related)

    # Toggler links
    related = related or []
    for child in primary_text.children:
        if child.slug in related:
            child.related = [r for r in related if r != child.slug]
        else:
            child.related = related + [child.slug]
        child.related = child.related or None

    return render_template('texts/segment.html', **data)


# API endpoints
# ~~~~~~~~~~~~~

@api.route('/texts/<slug>/<query>')
@api.route('/texts/<slug>/<query>+<list:related>')
def segment_api(slug, query, related=None):
    """API for querying segments.

    :param slug: the text's slug
    :param query: the query to perform
    :param related: if specified, a list of the slugs of related texts.
    """
    text = Text.query.filter(Text.slug == slug).first()
    if text is None:
        return jsonify({})

    data = segments_data(text, slug, query, related)
    return jsonify(data)


@api.route('/texts-child/<slug>/<list:ids>')
def child_segment_api(slug, ids):

    return jsonify(child_segments_data(slug, ids))
