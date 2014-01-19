import pytest

from lso.database import Base
from lso.guide import setup
from lso.guide.models import Lesson


@pytest.fixture(scope='session')
def graph_data():
    return setup.build_graph()


@pytest.fixture(scope='session')
def lessons(engine, graph_data, sessionclass):
    Base.metadata.create_all(engine)
    setup.add_lessons(graph_data, sessionclass)
    return sessionclass().query(Lesson).all()


class TestData:

    """Verifies that the the lesson graph is well-formed"""

    def _unique(self, graph_data, key):
        error_msg = "Duplicate {} '{}'"
        seen = set()
        for lesson in graph_data:
            token = lesson[key]
            assert token not in seen, error_msg.format(key, token)
            seen.add(token)

    def test_unique_names(self, graph_data):
        self._unique(graph_data, 'name')

    def test_unique_slugs(self, graph_data):
        self._unique(graph_data, 'slug')

    def test_valid_deps(self, graph_data):
        error_msg = "Invalid dependency '{}' in '{}'"
        slugs = set(lesson['slug'] for lesson in graph_data)
        for lesson in graph_data:
            for dep in lesson['deps']:
                assert dep in slugs, error_msg.format(dep, lesson['name'])

    def test_no_circular_dependencies(self, graph_data):
        error_msg = "Circular dependency starting from '{}'."
        lesson_map = {L['slug']: L for L in graph_data}

        # O(n^2) is fast enough
        for lesson in graph_data:
            stack = list(lesson['deps'])
            while stack:
                other = lesson_map[stack.pop()]
                assert other != lesson, error_msg.format(lesson['name'])
                stack.extend(other['deps'])

    def test_mostly_no_deps(self, graph_data):
        """Verify that only a few lessons have no dependencesies."""
        no_deps = set(x['slug'] for x in graph_data if not x['deps'])
        assert no_deps == {'a', 'how-sanskrit-works'}


class TestAddLessons:

    """Verifies that the lesson graph has been stored correctly."""

    def test_all_defined(self, graph_data, lessons):
        assert len(lessons) == len(graph_data)

    def test_names_and_slugs(self, graph_data, lessons):
        for datum, lesson in zip(graph_data, lessons):
            assert lesson.name == datum['name']
            assert lesson.slug == datum['slug']

    def test_predecessors(self, graph_data, lessons):
        predecessor_map = {x['slug']: set(x['deps']) for x in graph_data}

        for lesson in lessons:
            predecessor_slugs = set([x.slug for x in lesson.predecessors()])
            assert predecessor_slugs == predecessor_map[lesson.slug]

    def test_successors(self, graph_data, lessons):
        successor_map = {x['slug']: set() for x in graph_data}
        for datum in graph_data:
            for dep in datum['deps']:
                successor_map[dep].add(datum['slug'])

        for lesson in lessons:
            successor_slugs = set([x.slug for x in lesson.successors()])
            assert successor_slugs == successor_map[lesson.slug]


class TestSlugify:

    def test_basic(self):
        assert setup.slugify('sanskrit') == 'sanskrit'

    def test_punctuation_inner(self):
        assert setup.slugify('a!@b') == 'a-b'

    def test_punctuation_outer(self):
        assert setup.slugify('`a`') == 'a'

    def test_uppercase(self):
        assert setup.slugify('Sanskrit') == 'sanskrit'

    def test_whitespace(self):
        assert setup.slugify('Sanskrit grammar') == 'sanskrit-grammar'
