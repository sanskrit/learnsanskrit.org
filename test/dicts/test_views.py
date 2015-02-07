# -*- encoding: utf-8 -*-
import json

import pytest

from lso.dicts import setup


@pytest.fixture(scope='module')
def mw_data(app):
    setup.run(app=app)


def test_main_single_word_with_entries(mw_data, test_app):
    results = test_app.get('/dicts/mw/q-hk/atha').data
    assert 'an auspicious and inceptive particle' in results


def test_main_single_word_no_entries(mw_data, test_app):
    results = test_app.get('/dicts/mw/q-hk/garbage').data
    assert 'No results found' in results


def test_main_multiple_words(mw_data, test_app):
    results = test_app.get('/api/mw/nara+aTa').data
    assert 'an auspicious and inceptive particle' in results
    assert 'a man, a male, a person' in results


def test_main_empty_word(mw_data, test_app):
    results = test_app.get('/api/mw/nara++aTa').data
    assert 'an auspicious and inceptive particle' in results
    assert 'a man, a male, a person' in results


def test_main_single_word_devanagari(mw_data, test_app):
    results = test_app.get('/dicts/mw/q-devanagari/अथ').data
    assert 'an auspicious and inceptive particle' in results


def test_api_single_word_with_entries(mw_data, test_app):
    results = json.loads(test_app.get('/api/mw/nara').data)
    assert results['nara']


def test_api_single_word_no_entries(mw_data, test_app):
    results = json.loads(test_app.get('/api/mw/garbage').data)
    assert results == {'garbage': []}


def test_api_multiple_words(mw_data, test_app):
    results = json.loads(test_app.get('/api/mw/nara+aTa').data)
    assert results['nara']
    assert results['aTa']


def test_api_empty_word(mw_data, test_app):
    results = json.loads(test_app.get('/api/mw/nara++aTa').data)
    assert results['nara']
    assert results['aTa']


# API queries are SLP1 only -> no tests for Devanagari
