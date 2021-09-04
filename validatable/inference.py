import datetime as dt
import decimal
import enum
import ipaddress
import numbers
import pathlib
import uuid

import sqlalchemy as sa
from pydantic import EmailStr, NameEmail
from pydantic.fields import ModelField
from pydantic.networks import IPvAnyAddress, IPvAnyInterface, IPvAnyNetwork
from pydantic.types import ConstrainedStr

from validatable.generic_types import GUID, Stringfy


def prepare_column_name(column: sa.Column, column_name: str) -> sa.Column:
    if column.name == column_name:
        return column

    if column.name is None:
        column.name = column_name
        return column

    raise ValueError(
        "Column name must be equal to field name, or field alias, or None"
    )


def from_str_to_sqlalchemy_type(python_type: type, m: ModelField):
    if m.field_info.max_length:
        return sa.String(m.field_info.max_length)
    if issubclass(python_type, ConstrainedStr):
        length = python_type.max_length or python_type.curtail_length
        return sa.String(length)

    if issubclass(python_type, EmailStr):
        return sa.String(320)

    return Stringfy


def from_number_to_sqlalchemy_type(python_type: type, m: ModelField):

    if issubclass(python_type, int):
        return sa.Integer

    if issubclass(python_type, float):
        return sa.Float

    if issubclass(python_type, decimal.Decimal):
        return sa.Numeric

    raise TypeError(
        "cannot infer sqlalchemy type for {}".format(repr(python_type))
    )


def from_ipaddress_to_sqlalchemy_type(python_type: type, m: ModelField):

    if issubclass(python_type, ipaddress._BaseV4):
        return Stringfy

    if issubclass(
        python_type,
        (ipaddress._BaseV6, IPvAnyAddress, IPvAnyNetwork, IPvAnyInterface),
    ):
        return Stringfy

    raise TypeError(
        "cannot infer sqlalchemy type for {}".format(repr(python_type))
    )


def from_datetimes_to_sqlalchemy_type(python_type: type, m: ModelField):

    if issubclass(python_type, dt.datetime):
        return sa.DateTime

    if issubclass(python_type, dt.date):
        return sa.Date

    if issubclass(python_type, dt.time):
        return sa.Time

    if issubclass(python_type, dt.timedelta):
        return sa.Interval

    raise TypeError(
        "cannot infer sqlalchemy type for {}".format(repr(python_type))
    )


def get_column(m: ModelField) -> sa.Column:
    column_name = m.alias
    col_kwargs = {
        k[3:]: v for k, v in m.field_info.extra.items() if k.startswith("sa_")
    }
    column = col_kwargs.pop("column", None)
    if isinstance(column, sa.Column):
        return prepare_column_name(column, column_name)

    column_type = col_kwargs.pop("type", None) or col_kwargs.pop("type_", None)
    if column_type:
        return sa.Column(column_name, column_type, **col_kwargs)

    python_type = m.type_

    if issubclass(python_type, numbers.Number):
        sa_type = from_number_to_sqlalchemy_type(python_type, m)
        return sa.Column(column_name, sa_type, **col_kwargs)

    if issubclass(python_type, (str, NameEmail, pathlib.Path)):
        sa_type = from_str_to_sqlalchemy_type(python_type, m)
        return sa.Column(column_name, sa_type, **col_kwargs)

    if issubclass(python_type, uuid.UUID):
        return sa.Column(column_name, GUID, **col_kwargs)

    if issubclass(python_type, (dt.date, dt.time, dt.timedelta)):
        sa_type = from_datetimes_to_sqlalchemy_type(python_type, m)
        return sa.Column(column_name, sa_type, **col_kwargs)

    if issubclass(python_type, bytes):
        return sa.Column(column_name, sa.LargeBinary, **col_kwargs)

    if issubclass(python_type, enum.Enum):
        return sa.Column(column_name, sa.Enum(python_type), **col_kwargs)

    if issubclass(python_type, ipaddress._IPAddressBase):
        sa_type = from_ipaddress_to_sqlalchemy_type(python_type, m)
        return sa.Column(column_name, sa_type, **col_kwargs)

    raise TypeError(
        "cannot infer sqlalchemy type for {}".format(repr(python_type))
    )
