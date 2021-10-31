"""Views for vyakarana-pravesha.

These views and templates substantially overlap with views.guide.
"""

from datetime import datetime

from lso.book_api import API

from flask import Blueprint, render_template


bp = Blueprint("vyakarana", __name__, url_prefix="/vyakarana")


@bp.route("/")
def index():
    guide = API.vyakarana()
    latest_mtime = guide.latest_mtime
    latest = datetime.fromtimestamp(latest_mtime).strftime("%d %B %Y")
    next = guide.topics[0].lessons[0]
    return render_template(
        "vyakarana/index.html", guide=guide, last_updated=latest, next=next
    )


@bp.route("/<slug>/")
def topic(slug):
    guide = API.vyakarana()
    topic = guide.topic(slug)
    prev = guide.prev_topic(slug)
    if prev:
        prev = prev.lessons[-1]
    next = topic.lessons[0]
    return render_template("vyakarana/topic.html", topic=topic, prev=prev, next=next)


@bp.route("/<topic>/<slug>/")
def lesson(topic, slug):
    guide = API.vyakarana()
    t = guide.topic(topic)
    lesson = t.lesson(slug)
    prev = guide.previous(t.slug, lesson.slug)
    next = guide.next(t.slug, lesson.slug)
    return render_template(
        "vyakarana/lesson.html", topic=t, lesson=lesson, prev=prev, next=next
    )
