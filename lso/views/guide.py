"""The new grammar guide."""

from datetime import datetime

from lso.book_api import API

from flask import Blueprint, render_template


bp = Blueprint("guide", __name__, url_prefix="/guide")


@bp.route("/")
def index():
    guide = API.guide()
    latest_mtime = guide.latest_mtime
    latest = datetime.fromtimestamp(latest_mtime).strftime("%d %B %Y")
    next = guide.topics[0].lessons[0]
    return render_template(
        "guide/index.html", guide=guide, last_updated=latest, next=next
    )


@bp.route("/print/cover/")
def print_cover():
    return "Sanskrit for beginners"


@bp.route("/print/all/")
def print_all():
    """For debugging. The entire guide at once."""
    guide = API.guide()
    latest_mtime = guide.latest_mtime
    latest = datetime.fromtimestamp(latest_mtime).strftime("%d %B %Y")
    next = guide.topics[0].lessons[0]
    return render_template(
        "guide/all.html",
        guide=guide,
    )


@bp.route("/<slug>/")
def topic(slug):
    guide = API.guide()
    topic = guide.topic(slug)
    prev = guide.prev_topic(slug)
    if prev:
        prev = prev.lessons[-1]
    try:
        next = topic.lessons[0]
    except IndexError:
        next = guide.next_topic(topic)
    return render_template("guide/topic.html", topic=topic, prev=prev, next=next)


@bp.route("/<topic>/<slug>/")
def lesson(topic, slug):
    guide = API.guide()
    t = guide.topic(topic)
    lesson = t.lesson(slug)
    prev = guide.previous(t.slug, lesson.slug)
    next = guide.next(t.slug, lesson.slug)
    return render_template(
        "guide/lesson.html", topic=t, lesson=lesson, prev=prev, next=next
    )
