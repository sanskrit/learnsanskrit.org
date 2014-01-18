from lso.guide import setup

import pytest


@pytest.fixture(scope='session')
def json_data():
    return setup.build_graph()


class TestData:

    """Verifies that the the lesson graph is well-formed"""

    def _unique(self, json_data, key):
        error_msg = "Duplicate {} '{}'"
        seen = set()
        for lesson in json_data:
            token = lesson[key]
            assert token not in seen, error_msg.format(key, token)
            seen.add(token)

    def test_unique_names(self, json_data):
        self._unique(json_data, 'name')

    def test_unique_slugs(self, json_data):
        self._unique(json_data, 'slug')

    def test_valid_deps(self, json_data):
        error_msg = "Invalid dependency '{}' in '{}'"
        slugs = set(lesson['slug'] for lesson in json_data)
        for lesson in json_data:
            for dep in lesson['deps']:
                assert dep in slugs, error_msg.format(dep, lesson['name'])

    def test_no_circular_dependencies(self, json_data):
        error_msg = "Circular dependency starting from '{}'."
        lesson_map = {L['slug']: L for L in json_data}

        # O(n^2) is fast enough
        for lesson in json_data:
            stack = list(lesson['deps'])
            while stack:
                other = lesson_map[stack.pop()]
                assert other != lesson, error_msg.format(lesson['name'])
                stack.extend(other['deps'])

    def test_mostly_no_deps(self, json_data):
        """Verify that only a few lessons have no dependencesies."""
        no_deps = set(x['slug'] for x in json_data if not x['deps'])
        assert no_deps == {'a', 'how-sanskrit-works'}


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
