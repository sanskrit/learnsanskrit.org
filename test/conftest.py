import pytest
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope='session')
def engine():
    return create_engine('sqlite://')


@pytest.fixture(scope='session')
def sessionclass(engine):
    return sessionmaker(bind=engine)


@pytest.fixture(scope='function')
def session(sessionclass):
    return sessionclass()
