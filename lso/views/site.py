"""General or legacy views

I first created this file while porting the old site to a static Flask build.
It also contains some generic views, such as the site contact form.
"""

import functools
import os

from flask import Blueprint, render_template

from lso import data


bp = Blueprint("site", __name__)


def get_folder(url_rule) -> str:
    tokens = str(url_rule).split("/")
    for t in tokens:
        if t:
            return t


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/errors/404.html")
def site_404():
    # Used by httpd conf in production
    return render_template("404.html")


@bp.route("/google00e79fa9dc122ab2.html")
def google():
    return render_template("google.html")


@bp.route("/contact/")
def contact():
    return render_template("contact.html")


@bp.route("/resources/")
def resources():
    return render_template("resources.html")


@bp.route("/supp/")
def supp():
    return render_template("supp.html")


@bp.route("/tools/")
def tools():
    return render_template("tools.html")


@bp.route("/use/")
def use():
    return render_template("use.html")


@bp.route("/mobile/menu/")
def mobile_menu():
    menu_items = [
        ("Home", "site.index"),
        ("Grammar", "guide.index"),
        ("Resources", "site.resources"),
        ("Tools", "site.tools"),
        ("Contact", "site.contact"),
    ]
    return render_template("mobile/menu.html", items=menu_items)


@bp.route("/grammar/")
def grammar():
    toc = data.TABLE_OF_CONTENTS
    return render_template("grammar/index.html", toc=toc)


@functools.cache
def get_inorder_urls():
    toc = data.TABLE_OF_CONTENTS
    urls = []
    for section in toc:
        urls.append(section.url)
        for chapter in section.children:
            urls.append(chapter.url)
            for lesson in chapter.children:
                urls.append(lesson.url)
    return urls


def get_prev_and_next(url: str):
    urls = get_inorder_urls()

    for i, cur in enumerate(urls):
        if cur == url:
            break
    prev = urls[i - 1] if i > 0 else None
    next = urls[i + 1] if i < len(urls) - 1 else None

    return prev, next


@bp.route("/<section>/")
def grammar_section(section):
    path = os.path.join("grammar", section, "index.html")

    url = "/".join(("", section))
    prev, next = get_prev_and_next(url)
    return render_template(path, prev=prev, next=next)


@bp.route("/<section>/<chapter>/")
def grammar_chapter(section, chapter):
    path = os.path.join("grammar", section, chapter, "index.html")

    url = "/".join(("", section, chapter))
    prev, next = get_prev_and_next(url)
    return render_template(path, prev=prev, next=next)


@bp.route("/<section>/<chapter>/<lesson>/")
def grammar_lesson(section, chapter, lesson):
    path = os.path.join("grammar", section, chapter, lesson, "index.html")

    url = "/".join(("", section, chapter, lesson))
    prev, next = get_prev_and_next(url)
    return render_template(path, prev=prev, next=next)


@bp.route("/texts/ashtadhyayi/book1-1/")
def ashtadhyayi_legacy():
    return render_template("texts/ashtadhyayi/book1-1.html")
