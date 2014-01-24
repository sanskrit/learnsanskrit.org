import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lso import app as _app


@pytest.fixture(scope='session')
def app(request):
    return _app.test_client()


@pytest.fixture(scope='session')
def engine():
    return create_engine('sqlite://')


@pytest.fixture(scope='session')
def sessionclass(engine):
    return sessionmaker(bind=engine)


@pytest.fixture(scope='function')
def session(sessionclass):
    return sessionclass()
