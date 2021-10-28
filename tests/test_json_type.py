from datetime import datetime
from uuid import uuid4

import pytest
import sqlalchemy as sa
from pydantic import BaseModel, Json

from validatable import UUID4, BaseTable, Field, MetaData, create_engine


class JsonCase(BaseModel):
    id: int = 1
    name: str = "json case"
    created_ts: datetime = datetime.now()


metadata = MetaData()


def test_json_type():
    class TableJson(BaseTable, metadata=metadata):
        id: UUID4 = Field(default_factory=uuid4, sa_primary_key=True)
        json_field: Json

    assert isinstance(TableJson.__sa_table__, sa.Table)


@pytest.mark.parametrize(
    "valid_json",
    [
        b'{"name":"John", "age":30, "car":null}',
        b'{"employees":["John", "Anna", "Peter"]}',
        b"[1, 2, 3]",
        JsonCase().json(),
    ],
    ids=[0, 1, 2, 3],
)
def test_json_type_db(valid_json):
    metadata = MetaData()

    class TableJson(BaseTable, metadata=metadata):
        id: UUID4 = Field(default_factory=uuid4, sa_primary_key=True)
        data: Json

    model = TableJson(data=valid_json)

    engine = create_engine("sqlite:///:memory:")

    metadata.create_all(engine)
    with engine.connect() as conn:
        insert = TableJson.t.insert().values(model.dict())
        conn.execute(insert)
        result = conn.execute(TableJson.t.select())
        data = result.fetchone()
        m = TableJson.parse_obj(data)

    assert model == m


def test_json_type_parameterised():
    class TableJsonWrapper(BaseTable, metadata=metadata):
        id: UUID4 = Field(default_factory=uuid4, sa_primary_key=True)
        json_field: Json[JsonCase]

    assert isinstance(TableJsonWrapper.t, sa.Table)


def test_json_type_parameterised_db():
    metadata = MetaData()

    class TableJsonWrapper(BaseTable, metadata=metadata):
        id: UUID4 = Field(default_factory=uuid4, sa_primary_key=True)
        json_field: Json[JsonCase]

    model = TableJsonWrapper(json_field=JsonCase().json())

    engine = create_engine("sqlite:///:memory:")

    metadata.create_all(engine)
    with engine.connect() as conn:
        insert = TableJsonWrapper.t.insert().values(model.dict())
        conn.execute(insert)
        result = conn.execute(TableJsonWrapper.t.select())
        data = result.fetchone()
        m = TableJsonWrapper.parse_obj(data)

    assert model == m
