"""Lesson API.

This API manages the tree structure of /guide and /vyakarana.
"""

import json
import os
import re

from typing import List, Optional, Dict

from flask import url_for

import lso.sml.render as render_sml


app_dir = os.path.dirname(__file__)
project_dir = os.path.dirname(app_dir)
GUIDE_DIR = os.path.join(project_dir, "content", "guide")
VYAK_DIR = os.path.join(project_dir, "content", "vyakarana")
GUIDE = None
CACHE = {}


class Lesson:
    title: str
    topic_slug: str
    slug: str
    content: str

    @staticmethod
    def load(directory, topic, lesson) -> Dict[str, str]:
        lesson_file = os.path.join(directory, f"{topic}/{lesson}.txt")
        mtime = os.path.getmtime(lesson_file)
        cache_key = (topic, lesson)
        try:
            res, ts = CACHE.get(cache_key)
            if ts >= mtime:
                return res, mtime
        except TypeError:
            pass
        with open(lesson_file) as f:
            raw = f.read()

        data = render_sml.render(raw)
        CACHE[cache_key] = (data, mtime)
        return data, mtime

    def __init__(self, directory, topic_slug, slug):
        self.topic_slug = topic_slug
        self.slug = slug
        self.directory = directory

        data, mtime = self.load(directory, topic_slug, slug)
        self.mtime = mtime
        self.title = data["title"]
        self.content = data["content"]

    @property
    def title_no_html(self):
        """Title with all HTML removed. Hacky."""
        return re.sub("<.*?>", "", self.title)

    @property
    def url(self):
        if "vyakarana" in self.directory:
            return url_for("vyakarana.lesson", topic=self.topic_slug, slug=self.slug)
        if "guide" in self.directory:
            return url_for("guide.lesson", topic=self.topic_slug, slug=self.slug)
        raise Exception(f"unknown directory {directory}")


class Topic:

    #: The full topic title (e.g. "Nominals 1: Normal stems")
    title: str
    #: A shortened version of the title that can fit in UI elements like
    #: breadcrumbs (e.g. "Nominals 1"). If not provided explicitly, this
    #: defaults to `title`.
    short_title: str
    #: The URL encoding of this topic (e.g. "nominals-1")
    slug: str
    #: Ordered list of lesson slugs for this topic. For each slug
    #: `lesson_slug`, we expect to find a file:
    #: `{topic_slug}/{lesson_slug}.txt`.
    lesson_slugs: List[str]

    def __init__(self, directory, slug):
        self.directory = directory
        self.slug = slug

        with open(os.path.join(directory, f"{self.slug}/index.json")) as f:
            data = json.load(f)
        self.title = data["title"]
        self.short_title = data.get("short_title", self.title)
        self.lesson_slugs = data["lessons"]

    @property
    def lessons(self) -> List[Lesson]:
        return [Lesson(self.directory, self.slug, x) for x in self.lesson_slugs]

    def lesson(self, slug) -> Optional[Lesson]:
        for L in self.lessons:
            if L.slug == slug:
                return L
        return None

    @property
    def title_no_html(self):
        """Title with all HTML removed. Hacky."""
        return re.sub("<.*?>", "", render_sml.render_inline(self.title))

    @property
    def url(self):
        if "vyakarana" in self.directory:
            return url_for("vyakarana.topic", slug=self.slug)
        if "guide" in self.directory:
            return url_for("guide.topic", slug=self.slug)
        raise Exception(f"unknown directory {directory}")


class API:

    topic_slugs: List[str]

    @staticmethod
    def guide():
        return API(GUIDE_DIR)

    @staticmethod
    def vyakarana():
        return API(VYAK_DIR)

    def __init__(self, directory):
        with open(os.path.join(directory, "index.json")) as f:
            data = json.load(f)
        self.directory = directory
        self.topic_slugs = data["topics"]

    def _iter_lessons(self):
        for t in self.topics:
            for L in t.lessons:
                yield L

    @property
    def latest_mtime(self):
        return max(L.mtime for L in self._iter_lessons())

    @property
    def topics(self) -> List[Topic]:
        return [Topic(self.directory, slug) for slug in self.topic_slugs]

    def topic(self, slug) -> Optional[Topic]:
        for t in self.topics:
            if t.slug == slug:
                return t
        return None

    def prev_topic(self, slug: str) -> Optional[Topic]:
        for i, t in enumerate(self.topics):
            if t.slug == slug:
                break
        if i:
            return self.topics[i - 1]
        else:
            return None

    def next_topic(self, slug: str) -> Optional[Topic]:
        for i, t in enumerate(self.topics):
            if t.slug == slug:
                break
        try:
            return self.topics[i + 1]
        except IndexError:
            return None

    def prev_lesson(self, topic, lesson) -> Optional[Lesson]:
        """Previous lesson, skipping topics."""
        all_lessons = list(self._iter_lessons())
        for i, L in enumerate(all_lessons):
            if L.topic_slug == topic and L.slug == lesson:
                break
        if i:
            return all_lessons[i - 1]
        else:
            return None

    def next_lesson(self, topic, lesson) -> Optional[Lesson]:
        """Next lesson, skipping topics."""
        all_lessons = list(self._iter_lessons())
        for i, L in enumerate(all_lessons):
            if L.topic_slug == topic and L.slug == lesson:
                break
        try:
            return all_lessons[i + 1]
        except IndexError:
            return None

    def previous(self, topic, lesson):
        """Previous lesson or topic."""
        ret = self.prev_lesson(topic, lesson)
        if ret and ret.topic_slug == topic:
            # Prev lesson
            return ret
        else:
            # First in topic --> return topic
            return self.topic(topic)

    def next(self, topic, lesson):
        """Next lesson or topic."""
        ret = self.next_lesson(topic, lesson)
        if ret and ret.topic_slug == topic:
            # Next lesson
            return ret
        else:
            # Last in topic --> return next topic
            return self.next_topic(topic)
