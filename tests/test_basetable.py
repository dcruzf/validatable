import uuid

import pytest
import sqlalchemy as sa
from conftest import metadata
from faker import Faker

from validatable import UUID4, BaseTable, Field

Faker.seed(0)
faker = Faker()


@pytest.fixture(scope="function")
def conn(engine):
    metadata.create_all(engine)
    with engine.connect() as conn:
        yield conn
    metadata.drop_all(engine)


class Base(BaseTable):
    id: UUID4 = Field(default_factory=uuid.uuid4, sa_primary_key=True)
    metadata = metadata


class ModelUpdateDelete(Base):
    num: int = 0


def test_metadata_property():

    meta = sa.MetaData()

    class ModelCase(BaseTable, metadata=meta):
        id: int = Field(sa_primary_key=True)

    class Base(BaseTable):
        metadata = meta
        id: int = Field(sa_primary_key=True)

    class TableFromBase(Base):
        ...

    class Table(BaseTable):
        __sa_metadata__ = meta
        id: int = Field(sa_primary_key=True)

    assert TableFromBase.metadata == meta
    assert ModelCase.metadata == meta
    assert Table.metadata == meta


def test_table_declaration():

    table = sa.Table(
        "modelcase",
        metadata,
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    )

    class ModelCase(BaseTable):

        __sa_table__ = table
        id: int = None

    assert table == ModelCase.__sa_table__


def test_raise_for_wrong_metadata():

    with pytest.raises(TypeError):

        class ModelCase(BaseTable, metadata="NotMetaData"):
            id: int = None


def test_database_update(conn):
    model = ModelUpdateDelete()
    insert = ModelUpdateDelete.insert().values(model.dict())

    update = (
        ModelUpdateDelete.update()
        .where(ModelUpdateDelete.c.id == model.id)
        .values(num=5)
    )
    one = ModelUpdateDelete.select().where(ModelUpdateDelete.c.id == model.id)

    conn.execute(insert)

    conn.execute(update)
    result_updated = conn.execute(one)
    data_updated = result_updated.fetchone()
    model_updated = ModelUpdateDelete.parse_obj(data_updated)

    assert model_updated.id == model.id
    assert model_updated.num != model.num
    assert model_updated.num == 5


def test_database_delete(conn):
    model = ModelUpdateDelete()
    insert = ModelUpdateDelete.insert().values(model.dict())
    c = model.c

    delete = ModelUpdateDelete.delete().where(c.id == model.id)
    query = ModelUpdateDelete.select()

    conn.execute(insert)
    results = conn.execute(query)
    data_before_delete = results.fetchall()
    conn.execute(delete)
    results = conn.execute(query)
    data_after_delete = results.fetchall()

    assert len(data_before_delete) == 1
    assert len(data_after_delete) == 0


class LeftTable(Base):
    a: str = "a"


class RightTable(Base):
    b: str = "b"
    left_id: UUID4 = Field(
        sa_args=[sa.ForeignKey(LeftTable.c.id)]  # type: ignore[attr-defined]
    )


def test_database_join_with_pydantic_model(conn):

    left = LeftTable()
    insert_left = LeftTable.insert().values(left.dict())
    conn.execute(insert_left)

    right = RightTable(left_id=left.id)
    insert_right = RightTable.insert().values(right.dict())
    conn.execute(insert_right)

    join = RightTable.join(LeftTable, LeftTable.c.id == RightTable.c.left_id)
    query = sa.select([*RightTable.c, *LeftTable.c]).select_from(join)

    result_join = conn.execute(query)
    data = result_join.fetchall()

    assert data[0][0] == right.id
    assert data[0][2] == left.id


def test_database_join_with_table(conn):

    left = LeftTable()
    insert_left = LeftTable.insert().values(left.dict())
    conn.execute(insert_left)

    right = RightTable(left_id=left.id)
    insert_right = RightTable.insert().values(right.dict())
    conn.execute(insert_right)

    join = RightTable.join(
        LeftTable.__sa_table__, LeftTable.c.id == RightTable.c.left_id
    )
    query = sa.select([*RightTable.c, *LeftTable.c]).select_from(join)

    result_join = conn.execute(query)
    data = result_join.fetchall()

    assert data[0][0] == right.id
    assert data[0][2] == left.id
