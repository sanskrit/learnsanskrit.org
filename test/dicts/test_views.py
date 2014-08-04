import json

import pytest

from lso.dicts import setup


@pytest.fixture(scope='module')
def mw_data(app):
    setup.run(app=app)


def test_api_single_word_with_entries(mw_data, test_app):
    results = json.loads(test_app.get('/api/mw/aham').data)
    assert results['aham']


def test_api_single_word_no_entries(mw_data, test_app):
    results = json.loads(test_app.get('/api/mw/garbage').data)
    assert results == {'garbage': []}


def test_api_multiple_words(mw_data, test_app):
    results = json.loads(test_app.get('/api/mw/aham+aTa').data)
    assert results['aham']
    assert results['aTa']
