import json

import pytest

from lso.dicts import setup


@pytest.fixture(scope='module')
def mw_data(app):
    setup.run(app=app)


def test_login(test_app):
    results = test_app.get('/login/')
    assert 'Sign in' in results.data
