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


def get_column(m: ModelField) -> sa.Column:  # noqa: C901
    col_name = m.alias
    python_type = m.type_
    col_kwargs = {
        k[3:]: v for k, v in m.field_info.extra.items() if k.startswith("sa_")
    }
    col = col_kwargs.pop("col", None)
    if col is not None:
        return col
    col_type = col_kwargs.pop("type", None)
    if col_type:
        return sa.Column(col_name, col_type, **col_kwargs)

    if issubclass(python_type, str):
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
                return sa.Column(
                    col_name, sa.String(max(length)), **col_kwargs
                )

        if m.field_info.max_length:
            return sa.Column(col_name, sa.String(m.max_length), **col_kwargs)

        return sa.Column(col_name, sa.Text, **col_kwargs)

    if issubclass(python_type, enum.Enum):
        return sa.Column(col_name, sa.Enum(python_type), **col_kwargs)

    if issubclass(python_type, int):
        return sa.Column(col_name, sa.BigInteger, **col_kwargs)

    if issubclass(python_type, float):
        return sa.Column(col_name, sa.Float, **col_kwargs)

    if issubclass(python_type, decimal.Decimal):
        return sa.Column(col_name, sa.Numeric, **col_kwargs)

    if issubclass(python_type, bytes):
        return sa.Column(col_name, sa.LargeBinary, **col_kwargs)

    col_type = type_map.get(python_type, None)
    if col_type:
        return sa.Column(col_name, col_type, **col_kwargs)
    raise TypeError(
        "cannot infer sqlalchemy type for {}".format(repr(python_type))
    )
