from flask import redirect, render_template, url_for
from sqlalchemy import and_

import lib as L
from . import texts
from .models import Text, Segment
from ..database import session


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
    d = divisions[0]
    print d.segments[-1]

    return render_template('texts/text.html', text=text,
                           divisions=divisions)


@texts.route('/<slug>/<query>')
def segment(slug, query):
    text = Text.query.filter(Text.slug == slug).first()
    if text is None:
        return redirect(url_for('.index'))

    segments = []
    path_groups = query.split(',')
    for g in path_groups:
        pre, cur, post = g.partition('-')

        # Path range
        if cur:
            pre = '.'.join((text.xmlid_prefix, pre))
            post = '.'.join((text.xmlid_prefix, post))
            results = Segment.query.filter(Segment.slug.in_([pre, post])).all()
            try:
                s1, s2 = results
                results = Segment.query.filter(and_(
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
            s_slug = '.'.join((text.xmlid_prefix, g))
            s = Segment.query.filter(Segment.slug == s_slug).first()
            if s:
                segments.append(s)

    print segments
    segments = [{'id': s.slug, 'data': L.transform(s.content)}
                for s in segments]
    return render_template('texts/segment.html', text=text,
                           segments=segments)
