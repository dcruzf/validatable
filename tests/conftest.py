import os

import pytest

from validatable import MetaData, create_engine

NUM_REPETITIONS = int(os.getenv("N") or 1)
DATABASE = os.getenv("DB") or "sqlite"
metadata = MetaData()


@pytest.fixture(scope="session")
def engine():

    if DATABASE == "sqlite":
        yield create_engine("sqlite:///:memory:")
    if DATABASE == "postgresql":
        yield create_engine(
            "postgresql://validatable:password@localhost:5432/db"
        )
    if DATABASE == "mariadb":
        yield create_engine(
            "mariadb+pymysql://validatable:password@localhost:3306/db"
        )


@pytest.fixture(scope="function")
def conn(engine):
    metadata.create_all(engine)
    with engine.connect() as conn:
        yield conn
    metadata.drop_all(engine)


class MakeConnection(object):
    def __init__(self, engine):
        self.engine = engine

    def __call__(self, model):
        self.metadata = model.__sa_metadata__
        self.metadata.create_all(self.engine)
        self.conn = self.engine.connect()
        return self.conn

    def close(self):
        self.conn.close()
        self.metadata.drop_all(self.engine)


@pytest.fixture()
def make_conn(engine):
    make_conn = MakeConnection(engine)
    yield make_conn
    make_conn.close()
