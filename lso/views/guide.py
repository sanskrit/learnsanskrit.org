"""The new grammar guide."""

from datetime import datetime

from lso.book_api import API

from flask import Blueprint, render_template


bp = Blueprint("guide", __name__, url_prefix="/guide")


def get_update_date():
    guide = API.guide()
    latest_mtime = guide.latest_mtime

    latest = datetime.fromtimestamp(latest_mtime).strftime("%d %B %Y")
    # Cross-platform hack to remove leading 0.
    if latest.startswith("0"):
        latest = latest[1:]
    return latest


@bp.route("/")
def index():
    guide = API.guide()
    next = guide.topics[0].lessons[0]
    last_updated = get_update_date()

    return render_template(
        "guide/index.html", guide=guide, last_updated=last_updated, next=next
    )


@bp.route("/print/")
def print():
    guide = API.guide()
    last_updated = get_update_date()
    return render_template(
        "guide/print/book.html",
        guide=guide,
        topics=guide.topics,
        last_updated=last_updated,
    )


@bp.route("/print-debug/")
def print_debug():
    """Special endpoint to quickly test print styles."""
    guide = API.guide()
    last_updated = get_update_date()
    return render_template(
        "guide/print/book.html",
        guide=guide,
        topics=guide.topics[:1],
        last_updated=last_updated,
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
