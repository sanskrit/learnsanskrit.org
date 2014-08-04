import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import lso
import lso.database

@pytest.fixture(scope='session')
def app(request):
    override = {
        'DATABASE_URI': 'sqlite://',
        'MONIER_DIR': os.path.join(os.path.dirname(__file__), 'data',
            'monier-williams'),
        'SQLALCHEMY_DATABASE_URI': 'sqlite://',
        'TESTING': True
    }
    app = lso.create_app(__name__, override)

    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='session')
def db(app):
    lso.database.db.create_all()
    return lso.database.db


@pytest.fixture(scope='session')
def test_app(app):
    return app.test_client()


@pytest.fixture(scope='session')
def engine(app, db):
    return db.engine


@pytest.fixture(scope='session')
def session(app, db):
    return db.session
