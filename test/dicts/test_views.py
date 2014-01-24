import json

import pytest


def test_api_single_word_with_entries(app):
    actual = json.loads(app.get('/api/mw/aham').data)
    assert actual['aham']


def test_api_single_word_no_entries(app):
    actual = json.loads(app.get('/api/mw/garbage').data)
    expected = {'garbage': []}
    assert actual == expected


def test_api_multiple_words(app):
    actual = json.loads(app.get('/api/mw/aham+aTa').data)
    assert actual['aham']
    assert actual['aTa']
