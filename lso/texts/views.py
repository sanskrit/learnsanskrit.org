from flask import redirect, render_template, url_for
from sqlalchemy import and_

import lib as L
from . import texts
from .models import Text, Segment


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
    texts = Text.query.all()
    return render_template('texts/index.html', texts=texts)


@texts.route('/<slug>/')
def title(slug):
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
def segment(slug, query):
    text = Text.query.filter(Text.slug == slug).first()
    if text is None:
        return redirect(url_for('.index'))

    # Segments
    segments = []
    path_groups = query.split(',')
    base_query = Segment.query.filter(Segment.text_id == text.id)
    for g in path_groups:
        pre, cur, post = g.partition('-')

        # Path range
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

        # Single path
        else:
            s = base_query.filter(Segment.slug == g).first()
            if s:
                segments.append(s)

    segments = [{'slug': s.slug,
                 'data': L.transform(s.content)}
                for s in segments]

    # Readable query
    readable_query = query.replace('-', ' - ').replace(',', ', ')
    readable_query = '%s %s' % (text.name, readable_query)

    return render_template('texts/segment.html', text=text,
                           readable_query=readable_query,
                           segments=segments)
