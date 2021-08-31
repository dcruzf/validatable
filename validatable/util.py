import datetime as dt
import decimal
import enum
import ipaddress
import pathlib

import sqlalchemy as sa
from pydantic.fields import ModelField
from pydantic.types import (
    ConstrainedBytes,
    ConstrainedDecimal,
    ConstrainedFloat,
    ConstrainedInt,
    ConstrainedStr,
)

type_map = {
    str: sa.String,
    ConstrainedStr: sa.String,
    float: sa.Float,
    ConstrainedFloat: sa.Float,
    bool: sa.Boolean,
    int: sa.Integer,
    ConstrainedInt: sa.Integer,
    bytes: sa.LargeBinary,
    ConstrainedBytes: sa.LargeBinary,
    dt.datetime: sa.DateTime,
    dt.date: sa.Date,
    dt.timedelta: sa.Interval,
    dt.time: sa.Time,
    ConstrainedDecimal: sa.Numeric,
    decimal.Decimal: sa.Numeric,
    ipaddress.IPv4Address: sa.String(15),
    ipaddress.IPv4Network: sa.String(31),
    ipaddress.IPv6Address: sa.String(39),
    ipaddress.IPv6Network: sa.String(43),
    pathlib.Path: sa.Text,
}


def prepare_column_name(column: sa.Column, column_name: str) -> sa.Column:
    if column.name == column_name:
        return column

    if column.name is None:
        column.name = column_name
        return column

    if column.name != column_name:
        raise ValueError(
            "Column name must be equal to field name, or field alias, or None"
        )


def from_str_to_sqlalchemy_type(python_type: type, m: ModelField):
    if m.field_info.max_length:
        return sa.String(m.field_info.max_length)
    if issubclass(python_type, ConstrainedStr):
        length = [
            length
            for length in [
                python_type.max_length,
                python_type.curtail_length,
            ]
            if length
        ]
        if length:
            return sa.String(max(length))
    return sa.Text


def get_column(m: ModelField) -> sa.Column:  # noqa: C901
    column_name = m.alias
    col_kwargs = {
        k[3:]: v for k, v in m.field_info.extra.items() if k.startswith("sa_")
    }
    column: sa.Column = col_kwargs.pop("column", None)
    if isinstance(column, sa.Column):
        return prepare_column_name(column, column_name)

    column_type = col_kwargs.pop("type", None) or col_kwargs.pop("type_", None)
    if column_type:
        return sa.Column(column_name, column_type, **col_kwargs)

    python_type = m.type_

    if issubclass(python_type, str):
        sa_type = from_str_to_sqlalchemy_type(python_type, m)
        return sa.Column(column_name, sa_type, **col_kwargs)

    if issubclass(python_type, enum.Enum):
        return sa.Column(column_name, sa.Enum(python_type), **col_kwargs)

    if issubclass(python_type, int):
        return sa.Column(column_name, sa.BigInteger, **col_kwargs)

    if issubclass(python_type, float):
        return sa.Column(column_name, sa.Float, **col_kwargs)

    if issubclass(python_type, decimal.Decimal):
        return sa.Column(column_name, sa.Numeric, **col_kwargs)

    if issubclass(python_type, bytes):
        return sa.Column(column_name, sa.LargeBinary, **col_kwargs)

    col_type = type_map.get(python_type, None)
    if col_type:
        return sa.Column(column_name, col_type, **col_kwargs)
    raise TypeError(
        "cannot infer sqlalchemy type for {}".format(repr(python_type))
    )
