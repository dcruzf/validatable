import datetime as dt
import decimal
import enum
import ipaddress
import numbers
import pathlib
import uuid
from typing import Any, Dict, List, Optional, Set, Tuple

import sqlalchemy as sa
from pydantic import EmailStr, NameEmail
from pydantic.fields import ModelField
from pydantic.networks import IPvAnyAddress, IPvAnyInterface, IPvAnyNetwork
from pydantic.types import ConstrainedBytes, ConstrainedDecimal, ConstrainedStr

from .generic_types import GUID, AutoString


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

    return AutoString


def from_bytes_to_sqlalchemy_type(python_type: type, m: ModelField):
    if m.field_info.max_length:
        return sa.LargeBinary(m.field_info.max_length)
    if issubclass(python_type, ConstrainedBytes):
        return sa.LargeBinary(python_type.max_length)

    return sa.LargeBinary


def from_number_to_sqlalchemy_type(python_type: type, m: ModelField):

    if issubclass(python_type, int):
        return sa.Integer

    if issubclass(python_type, float):
        return sa.Float

    if issubclass(python_type, ConstrainedDecimal):
        return sa.Numeric(
            precision=python_type.max_digits, scale=python_type.decimal_places
        )

    if issubclass(python_type, decimal.Decimal):
        return sa.Numeric

    raise TypeError(
        "cannot infer sqlalchemy type for {}".format(repr(python_type))
    )


def from_ipaddress_to_sqlalchemy_type(python_type: type, m: ModelField):

    if issubclass(python_type, ipaddress._BaseV4):  # type: ignore
        return AutoString

    if issubclass(
        python_type,
        (
            ipaddress._BaseV6,  # type: ignore
            IPvAnyAddress,
            IPvAnyNetwork,
            IPvAnyInterface,
        ),
    ):
        return AutoString

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

    return sa.Interval


def get_type(m: ModelField):

    if issubclass(m.type_, numbers.Number):
        return from_number_to_sqlalchemy_type(m.type_, m)

    if issubclass(m.type_, (str, NameEmail, pathlib.Path)):
        return from_str_to_sqlalchemy_type(m.type_, m)

    if issubclass(m.type_, uuid.UUID):
        return GUID

    if issubclass(m.type_, (dt.date, dt.time, dt.timedelta)):
        return from_datetimes_to_sqlalchemy_type(m.type_, m)

    if issubclass(m.type_, bytes):
        return from_bytes_to_sqlalchemy_type(m.type_, m)

    if issubclass(m.type_, enum.Enum):
        return sa.Enum(m.type_)

    if issubclass(m.type_, ipaddress._IPAddressBase):
        return from_ipaddress_to_sqlalchemy_type(m.type_, m)

    raise TypeError(
        "cannot infer sqlalchemy type for {}".format(repr(m.type_))
    )


def get_sa_args_kwargs(m: ModelField) -> Tuple[Any, Dict[str, Any]]:
    keys = tuple(m.field_info.extra.keys())
    col_kwargs = {
        k[3:]: m.field_info.extra.pop(k) for k in keys if k.startswith("sa_")
    }
    pk = col_kwargs.pop("pk", False)
    col_kwargs["primary_key"] = col_kwargs.get("primary_key") or pk
    args = col_kwargs.pop("args", [])
    fk = col_kwargs.pop("fk", None)
    fk = col_kwargs.pop("foreign_key", None) or fk
    args.append(fk)
    return args, col_kwargs


def get_column(m: ModelField) -> sa.Column:
    args, col_kwargs = get_sa_args_kwargs(m)
    column = col_kwargs.pop("column", None)

    if isinstance(column, sa.Column):
        return prepare_column_name(column, m.alias)

    column_type = col_kwargs.pop("type", None) or col_kwargs.pop("type_", None)

    if column_type:
        return sa.Column(m.alias, column_type, *args, **col_kwargs)

    sa_type = get_type(m)
    return sa.Column(m.alias, sa_type, *args, **col_kwargs)


def is_model_field(v: Any) -> bool:
    return hasattr(v, "__class__") and isinstance(v, ModelField)


def get_table(
    name: str,
    metadata: sa.MetaData,
    fields: Dict[str, Any],
    table_args: List[str],
    table_kwargs: Dict[str, Any],
    exclude: Optional[Set[str]] = None,
) -> sa.Table:

    exclude = exclude or set()
    columns = [
        get_column(v)
        for k, v in fields.items()
        if k not in exclude and is_model_field(v)
    ]
    return sa.Table(name, metadata, *columns, *table_args, **table_kwargs)
