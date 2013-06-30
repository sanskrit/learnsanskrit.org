from collections import defaultdict

from flask import (Blueprint, flash, redirect, render_template, url_for,
                   jsonify)
from sqlalchemy import and_

import lib as L
from lso import app
from .models import (Author, Category, Language, Segment,
                     SegSegAssoc as SSA, Text)

LANGUAGES = None
CATEGORIES = None
PAGE_SIZE = 5
MIN_PAGE_SIZE = 3


bp = Blueprint('texts', __name__, static_folder='static',
               template_folder='templates', url_prefix='/texts')


def _flash_missing_text(slug):
    flash("We can't find text \"%s\" in the collection." % slug)


def paginate(items, size, min_size=0):
    """Simple pagination.

    :param size: the group size
    :param min_size: the mininum group size. If a group is smaller than
                     `min_size`, then it is merged into the previous
                     group, if one exists.
    """
    groups = []
    for start in xrange(0, len(items), size):
        groups.append(items[start:start+size])

    try:
        if len(groups[-1]) < min_size:
            groups[-2].extend(groups[-1])
            groups.pop()
    except IndexError:
        pass
    return groups


def division_paginate(division, size, min_size):
    last_slug = division.segments[-1].slug.rpartition('.')[2]
    number = int(last_slug)
    slugs = ['%s.%s' % (division.slug, n) for n in range(1, number+1)]
    return paginate(slugs, size, min_size)


def peer_divisions(text, cur):
    divs = text.division.mp.query_descendants().all()
    return [d for d in divs if d.mp_depth == cur.mp_depth]


def page_to_query(page):
    p1, p2 = page[0], page[-1]
    if p1 == p2:
        return {'query': p1, 'readable': p1}
    else:
        return {'query': '-'.join((p1, p2)), 'readable': ' - '.join((p1, p2))}


@app.before_first_request
def load_data():
    global CATEGORIES, LANGUAGES
    CATEGORIES = {x.id: x.slug for x in Category.query.all()}
    LANGUAGES = {x.slug: x.id for x in Language.query.all()}


@bp.route('/')
def index():
    """A basic index page containing all texts in the collection."""

    texts = Text.query.filter(Text.language_id == LANGUAGES['sa'])\
                      .all()
    return render_template('texts/index.html', texts=texts)


@bp.route('/<slug>/')
def text(slug):
    """The main page of a given text.

    :param slug: the text's slug
    """
    text = Text.query.filter(Text.slug == slug).first()
    if text is None:
        _flash_missing_text(slug)
        return redirect(url_for('.index'))

    divs = text.division.mp.query_descendants().all()
    pages = []
    for d in divs:
        d_pages = division_paginate(d, PAGE_SIZE, min_size=MIN_PAGE_SIZE)
        d_pages = map(page_to_query, d_pages)
        pages.append(d_pages)

    return render_template('texts/text.html', text=text,
                           divs=divs,
                           pages=pages)


@app.route('/author/<slug>')
def author(slug):
    author = Author.query.filter(Author.slug == slug).first()
    return render_template('texts/author.html', author=author)


# Segment data
# ~~~~~~~~~~~~

def child_segments_data(child_slug, parent_ids):
    """

    :param child_slug: slug for the child text
    :param parent_ids: IDs of parent segments
    """
    data = defaultdict(lambda: defaultdict(list))

    # Find corresponding segments
    child = Text.query.filter(Text.slug == child_slug).one()
    results = SSA.query.filter(SSA.parent_id.in_(parent_ids))\
                       .filter(SSA.text_id==child.id).all()

    # Clean up data for display
    for r in results:
        seg = r.child
        xml_id = '.'.join((child.xmlid_prefix, seg.slug))
        content = L.transform(seg.content)
        datum = {
            'id': seg.id,
            'slug': seg.slug,
            'xmlid': xml_id,
            'content': content}
        data[r.parent_id][child_slug].append(datum)

    return data


def segments_data(text, slug, query, related):
    # Find the segments specified by `query`
    segments = []
    base_query = Segment.query.filter(Segment.text_id == text.id)\
                        .order_by(Segment.position.asc())
    query_groups = query.split(',')
    for g in query_groups:
        pre, cur, post = g.partition('-')

        # Slug range, e.g. '1.1-1.5'
        if cur:
            results = base_query.filter(Segment.slug.in_([pre, post])).all()
            try:
                s1, s2 = results
                results = base_query.filter(and_(
                    Segment.position > s1.position,
                    Segment.position < s2.position)).all()
                segments.append(s1)
                segments.extend(results)
                segments.append(s2)
            except ValueError:
                if results:
                    segments.append(results[0])

        # Single slug, e.g. '1.2'
        else:
            s = base_query.filter(Segment.slug == g).first()
            if s:
                segments.append(s)

    # Clean up data for display
    ids = [s.id for s in segments]
    xmlids = ['.'.join((text.xmlid_prefix, s.slug)) for s in segments]
    slugs = [s.slug for s in segments]
    contents = map(L.transform, (s.content for s in segments))

    clean_segments = [{'id': i, 'xmlid': x, 'slug': s, 'content': c}
                      for i, x, s, c in zip(ids, xmlids, slugs, contents)]

    # Find textual correspondences
    id_to_slug = {s.id: s.slug for s in segments}
    if related:
        clean_corresp = defaultdict(lambda: defaultdict(list))
        for grp in related:
            data = child_segments_data(grp, ids)
            for id in data:
                clean_corresp[id_to_slug[id]][grp] = data[id][grp]

    else:
        clean_corresp = None

    # Create "prev" and "next" links based on start, end of query
    if len(query_groups) == 1:
        first, last = segments[0], segments[-1]

        cur = first.division
        cur_pages = division_paginate(cur, PAGE_SIZE, MIN_PAGE_SIZE)
        divs = None

        slug_index_map = {slug: (i, j) for i, page in enumerate(cur_pages)
                                       for j, slug in enumerate(page)}

        # prev
        i, j = slug_index_map[first.slug]
        # prev in current division
        if i:
            prev = cur_pages[i-1]
            if j:
                prev.extend(cur_pages[i][:j])
        # prev in previous division
        else:
            divs = divs or peer_divisions(text, cur)
            for k, d in enumerate(divs):
                if d.id == cur.id:
                    break
            if k:
                pages = division_paginate(divs[k-1], PAGE_SIZE, MIN_PAGE_SIZE)
                prev = pages[-1]
            else:
                prev = None

        # next
        i, j = slug_index_map[last.slug]
        next = cur_pages[i][j+1:]
        # next in current division
        try:
            if len(next) < MIN_PAGE_SIZE:
                next.extend(cur_pages[i+1])
        except IndexError:
            pass
        # next in next division
        if not next:
            divs = divs or peer_divisions(text, cur)
            for k, d in enumerate(divs):
                if d.id == cur.id:
                    break
            try:
                pages = division_paginate(divs[k+1], PAGE_SIZE, MIN_PAGE_SIZE)
                next = pages[0]
            except IndexError:
                next = None

        # convert to query form
        if prev:
            prev = page_to_query(prev)
        if next:
            next = page_to_query(next)
    else:
        prev = next = None

    # Rewrite the query in a human-readable form
    readable_query = query.replace('-', ' - ').replace(',', ', ')
    readable_query = '%s %s' % (text.name, readable_query)

    return dict(
        text=text,
        query=query,
        readable_query=readable_query,
        segments=clean_segments,
        corresp=clean_corresp,
        prev=prev,
        next=next,
        related=related
    )


@bp.route('/<slug>/<query>')
@bp.route('/<slug>/<query>+<list:related>')
def segment(slug, query, related=None):
    """Query a given text for a group of segments. If related texts are
    listed too, show their corresponding segments.

    :param slug: the text's slug
    :param query: the segment query to perform. This is a CSL of slug
                  groups, e.g. '1.2', '1.1-1.5', and so on.
    :param related: if specified, a CSL of the slugs of related texts.
    """

    # Main text
    text = Text.query.filter(Text.slug == slug).first()
    if text is None:
        _flash_missing_text(slug)
        return redirect(url_for('.index'))

    # Data
    data = segments_data(text, slug, query, related)

    # Child texts
    data['translation'] = []
    data['commentary'] = []

    children = Text.query.filter(Text.parent_id == text.id).all()
    for c in children:
        key = CATEGORIES[c.category_id]
        data[key].append(c)

    # 'related' of child texts
    related = related or []
    for c in children:
        if c.slug in related:
            c.related = [r for r in related if r != c.slug]
        else:
            c.related = related + [c.slug]
        c.related = c.related or None

    return render_template('texts/segment.html', **data)


# API endpoints
# ~~~~~~~~~~~~~

@app.route('/api/texts/<slug>/<query>')
@app.route('/api/texts/<slug>/<query>+<list:related>')
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
    data['text'] = {'slug': text.slug}
    return jsonify(data)


@app.route('/api/texts-child/<slug>/<list:ids>')
def child_segment_api(slug, ids):

    return jsonify(child_segments_data(slug, ids))
