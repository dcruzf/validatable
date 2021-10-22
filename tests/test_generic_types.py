from typing import Any, List, Set, Tuple
from uuid import UUID

import pytest
from sqlalchemy.dialects import mysql, postgresql, sqlite
from sqlalchemy.schema import Column, CreateColumn

from validatable.generic_types import GUID, AutoJson, AutoString, SLBigInteger


def test_guid_type_DDL_postgresql():
    c = Column("c", GUID)
    t_ddl = CreateColumn(c)

    postgresql_ddl = str(t_ddl.compile(dialect=postgresql.dialect()))
    _, postgresql_type = postgresql_ddl.split()

    assert "UUID" == postgresql_type


def test_guid_type_DDL_sqlite():
    c = Column("c", GUID)
    t_ddl = CreateColumn(c)

    sqlite_ddl = str(t_ddl.compile(dialect=sqlite.dialect()))
    _, sqlite_type = sqlite_ddl.split()

    assert "BINARY(16)" == sqlite_type


def test_guid_type_DDL_mysql():
    c = Column("c", GUID)
    t_ddl = CreateColumn(c)

    mysql_ddl = str(t_ddl.compile(dialect=mysql.dialect()))
    _, mysql_type = mysql_ddl.split()

    assert "BINARY(16)" == mysql_type


def test_guid_python_type():
    assert GUID().python_type == UUID


@pytest.mark.parametrize(
    ["value", "dialect", "expected"],
    (
        (
            [
                UUID("08e6ff8e253545d584558a50a57667c5"),
                "postgresql",
                UUID("08e6ff8e253545d584558a50a57667c5"),
            ],
            [
                None,
                "postgresql",
                None,
            ],
            [
                UUID("08e6ff8e253545d584558a50a57667c5"),
                "Any other",
                UUID("08e6ff8e253545d584558a50a57667c5").bytes,
            ],
            [
                None,
                "Any other",
                None,
            ],
        )
    ),
)
def test_guid_process_bind_param(value, dialect, expected):
    DialectMock = type("DialectMock", (object,), {"name": dialect})
    guid = GUID()
    result = guid.process_bind_param(value, DialectMock)
    assert result == expected


@pytest.mark.parametrize(
    ["value", "dialect", "expected"],
    (
        (
            [
                UUID("08e6ff8e253545d584558a50a57667c5"),
                "postgresql",
                UUID("08e6ff8e253545d584558a50a57667c5"),
            ],
            [
                None,
                "postgresql",
                None,
            ],
            [
                UUID("08e6ff8e253545d584558a50a57667c5").bytes,
                "Any other",
                UUID("08e6ff8e253545d584558a50a57667c5"),
            ],
            [
                None,
                "Any other",
                None,
            ],
        )
    ),
)
def test_guid_process_result_value(value, dialect, expected):
    DialectMock = type("DialectMock", (object,), {"name": dialect})
    guid = GUID()
    result = guid.process_result_value(value, DialectMock)
    assert result == expected


def test_autostring_python_type():
    assert AutoString().python_type == str


def test_autostring_type_DDL_postgresql():
    c = Column("c", AutoString)
    t_ddl = CreateColumn(c)

    postgresql_ddl = str(t_ddl.compile(dialect=postgresql.dialect()))
    _, postgresql_type = postgresql_ddl.split()

    assert "VARCHAR" == postgresql_type


def test_autostring_type_DDL_sqlite():
    c = Column("c", AutoString)
    t_ddl = CreateColumn(c)

    sqlite_ddl = str(t_ddl.compile(dialect=sqlite.dialect()))
    _, sqlite_type = sqlite_ddl.split()

    assert "VARCHAR" == sqlite_type


def test_autostring_type_DDL_mysql():
    c = Column("c", AutoString)
    t_ddl = CreateColumn(c)

    mysql_ddl = str(t_ddl.compile(dialect=mysql.dialect()))
    _, mysql_type = mysql_ddl.split()

    assert "VARCHAR(512)" == mysql_type


@pytest.mark.parametrize(
    ["value", "dialect", "expected"],
    (
        (
            [
                "SomeString",
                "Any",
                "SomeString",
            ],
            [
                None,
                "Any",
                None,
            ],
            [
                1,
                "Any",
                "1",
            ],
        )
    ),
)
def test_autostring_process_bind_param(value, dialect, expected):
    DialectMock = type("DialectMock", (object,), {"name": dialect})
    auto_string = AutoString()
    result = auto_string.process_bind_param(value, DialectMock)
    assert result == expected


@pytest.mark.parametrize(
    ["value", "dialect", "expected"],
    (
        (
            [
                "SomeString",
                "Any",
                "SomeString",
            ],
            [
                None,
                "Any",
                None,
            ],
        )
    ),
)
def test_autostring_process_result_value(value, dialect, expected):
    DialectMock = type("DialectMock", (object,), {"name": dialect})
    auto_string = AutoString()
    result = auto_string.process_result_value(value, DialectMock)
    assert result == expected


def test_slbiginteger_type_DDL_sqlite():
    c = Column("c", SLBigInteger)
    t_ddl = CreateColumn(c)

    sqlite_ddl = str(t_ddl.compile(dialect=sqlite.dialect()))
    _, sqlite_type = sqlite_ddl.split()

    assert "INTEGER" == sqlite_type


@pytest.mark.parametrize(
    "dialect, expected_type",
    [(sqlite, "INTEGER"), (mysql, "BIGINT"), (postgresql, "BIGINT")],
    ids=["sqlite", "mysql", "postgresql"],
)
def test_slbiginteger_type_DDL_not_sqlite(dialect, expected_type):
    c = Column("c", SLBigInteger)
    t_ddl = CreateColumn(c)

    dialect_ddl = str(t_ddl.compile(dialect=dialect.dialect()))
    _, dialect_type = dialect_ddl.split()

    assert dialect_type == expected_type


@pytest.mark.parametrize(
    "type_",
    [List, Any, Set, Tuple, list, set, tuple],
)
def test_autojson_python_type(type_):
    assert AutoJson(python_type=type_).python_type == type_
