from flask import redirect, render_template, url_for

import lib as L
from . import texts
from .models import Text, Segment


@texts.route('/')
def index():
    texts = Text.query.all()
    return render_template('texts/index.html', texts=texts)


@texts.route('/<slug>/')
def title(slug):
    text = Text.query.filter(Text.slug == slug).first()
    if text is None:
        return redirect(url_for('.index'))

    return render_template('texts/text.html', text=text)


@texts.route('/<text>/<path>')
def segment(text, path):
    slug = text
    text = Text.query.filter(Text.slug == slug).first()
    if text is None:
        return redirect(url_for('.index'))

    path = text.xmlid_prefix + '.' + path

    segments = Segment.query.filter(Segment.text_id == text.id)\
                            .filter(Segment.slug == path)\
                            .all()

    segments = [{'id': s.slug, 'data': L.transform(s.content)}
                for s in segments]
    return render_template('texts/segment.html', text=text,
                           segments=segments)
