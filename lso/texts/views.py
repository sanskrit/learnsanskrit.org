from collections import defaultdict

from flask import redirect, render_template, url_for
from sqlalchemy import and_

import lib as L
from . import texts
from .models import Language, Segment, SegSegAssoc as SSA, Text

LANG = None

def paginate(items, size, min_size=0):
    """Simple pagination.

    :param size: the group size
    :param min_size: the mininum group size. If a group is smaller than
                     `min_size`, then it is merged into the previous
                     group, if one exists.
    """
    groups = []
    i = 0
    for start in xrange(0, len(items), size):
        groups.append(items[start:start+size])
        i += 1

    if i > 2 and len(groups[-1]) < min_size:
        groups[-2].extend(groups[-1])
        groups.pop()
    return groups


@texts.route('/')
def index():
    """A basic index page containing all texts in the collection."""
    global LANG
    if LANG is None:
        LANG = {x.slug : x.id for x in Language.query.all()}

    texts = Text.query.filter(Text.language_id == LANG['sa'])\
                      .all()
    return render_template('texts/index.html', texts=texts)


@texts.route('/<slug>/')
def title(slug):
    """A title page for a given text.

    :param slug: the text's slug
    """
    text = Text.query.filter(Text.slug == slug).first()
    if text is None:
        return redirect(url_for('.index'))

    divisions = text.division.mp.query_descendants().all()
    pages = []
    for d in divisions:
        last_slug = d.segments[-1].slug.rpartition('.')[2]
        number = int(last_slug)
        slugs = ['%s.%s' % (d.slug, n) for n in range(1, number+1)]
        pages.append(paginate(slugs, 5, min_size=3))

    return render_template('texts/text.html', text=text,
                           divisions=divisions,
                           pages=pages)


@texts.route('/<slug>/<query>')
@texts.route('/<slug>/<query>+<related>')
def segment(slug, query, related=None):
    """Query a given text for a group of segments. If related texts are
    listed too, show their corresponding segments.

    :param slug: the text's slug
    :param query: the segment query to perform. This is a CSL of slug
                  groups, e.g. '1.2', '1.1-1.5', and so on.
    :param related: if specified, a CSL of the slugs of related texts.
    """
    text = Text.query.filter(Text.slug == slug).first()
    if text is None:
        return redirect(url_for('.index'))

    # Segments
    segments = []
    base_query = Segment.query.filter(Segment.text_id == text.id)\
                        .order_by(Segment.position.asc())
    for g in query.split(','):
        pre, cur, post = g.partition('-')

        # Slug range
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

        # Single slug
        else:
            s = base_query.filter(Segment.slug == g).first()
            if s:
                segments.append(s)

    # Clean up data for display
    ids = [s.id for s in segments]
    xmlids = ['.'.join((text.xmlid_prefix, s.slug)) for s in segments]
    slugs = [s.slug for s in segments]
    contents = map(L.transform, (s.content for s in segments))
    segments = [{'id': i, 'xmlid': x, 'slug': s, 'content': c}
                for i, x, s, c in zip(ids, xmlids, slugs, contents)]

    # Text correspondence
    id_to_slug = {s['id']: s['slug'] for s in segments}
    if related:
        corresp = defaultdict(lambda: defaultdict(list))
        for grp in related.split(','):
            # Find corresponding segments
            child = Text.query.filter(Text.slug == grp).one()
            results = SSA.query.filter(SSA.parent_id.in_(ids))\
                               .filter(SSA.text_id==child.id).all()

            # Process and store
            for r in results:
                xml_id = '.'.join((child.slug, r.child.slug))
                content = L.transform(r.child.content)
                data = {'id': xml_id, 'content': content}
                parent_slug = id_to_slug[r.parent_id]
                corresp[parent_slug][child.slug].append(data)
    else:
        corresp = None

    # Readable query
    readable_query = query.replace('-', ' - ').replace(',', ', ')
    readable_query = '%s %s' % (text.name, readable_query)

    return render_template('texts/segment.html', text=text,
                           readable_query=readable_query,
                           segments=segments,
                           corresp=corresp)
