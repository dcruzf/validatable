from typing import List

from pydantic import parse_obj_as

from validatable import BaseTable, Field, MetaData


def test_nullable_column():
    class NotNull(BaseTable, metadata=MetaData()):
        not_null: str

    table = NotNull.__sa_table__
    m = NotNull.__fields__["not_null"]

    assert m.required
    assert not table.c.not_null.nullable


def test_nullable_column_elipsis():
    class NotNull(BaseTable, metadata=MetaData()):
        id: int = Field(sa_pk=True)
        not_null: str = Field(...)

    table = NotNull.__sa_table__
    m = NotNull.__fields__["not_null"]

    assert m.required
    assert not table.c.not_null.nullable


def test_nullable_column_only_sql():
    class NotNull(BaseTable, metadata=MetaData()):
        not_null: str = Field(None, sa_nullable=False)

    table = NotNull.__sa_table__
    m = NotNull.__fields__["not_null"]

    assert not table.c.not_null.nullable
    assert not m.required


def test_nullable_column_with_pk():
    class NotNull(BaseTable, metadata=MetaData()):
        not_null: int = Field(None, sa_pk=True)

    table = NotNull.__sa_table__
    m = NotNull.__fields__["not_null"]

    assert table.c.not_null.nullable is None
    assert not m.required


def test_nullable_column_with_pk_integration(make_conn):
    class NotNull(BaseTable, metadata=MetaData()):
        id: int = Field(None, sa_pk=True)
        test: int = Field(..., sa_unique=True)

    data = [NotNull(test=n).dict() for n in (1, 2, 3)]
    conn = make_conn(NotNull)
    conn.execute(NotNull.t.insert().values(data))
    result = conn.execute(NotNull.t.select())
    db_data = result.fetchall()

    not_nulls = parse_obj_as(List[NotNull], db_data)

    assert len(db_data) == 3
    assert len(not_nulls) == 3
    assert all(n.id is not None for n in not_nulls)


def test_nullable_column_with_pk_integration_sa_nullable_true(make_conn):
    class NotNull(BaseTable, metadata=MetaData()):
        id: int = Field(..., sa_pk=True, sa_nullable=True)
        test: int = Field(..., sa_unique=True)

    data = [NotNull(test=n, id=n).dict() for n in (1, 2, 3)]
    conn = make_conn(NotNull)
    conn.execute(NotNull.t.insert().values(data))
    result = conn.execute(NotNull.t.select())
    db_data = result.fetchall()

    not_nulls = parse_obj_as(List[NotNull], db_data)

    assert len(db_data) == 3
    assert len(not_nulls) == 3
