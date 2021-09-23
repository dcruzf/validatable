import os

import pytest
import sqlalchemy as sa

NUM_TEST = int(os.getenv("N") or 1)
DATABASE = os.getenv("DB") or "sqlite"
metadata = sa.MetaData()


@pytest.fixture(scope="session")
def engine():

    if DATABASE == "sqlite":
        yield sa.create_engine("sqlite:///:memory:")
    if DATABASE == "postgresql":
        yield sa.create_engine(
            "postgresql://validatable:password@localhost:5432/db"
        )
    if DATABASE == "mariadb":
        yield sa.create_engine(
            "mariadb+pymysql://validatable:password@localhost:3306/db"
        )


@pytest.fixture(scope="function")
def conn(engine):
    metadata.create_all(engine)
    with engine.connect() as conn:
        yield conn
    metadata.drop_all(engine)
