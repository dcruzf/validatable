import datetime as dt
import enum
import pathlib
import uuid
from decimal import Decimal
from ipaddress import (
    IPv4Address,
    IPv4Interface,
    IPv4Network,
    IPv6Address,
    IPv6Interface,
    IPv6Network,
)

import pytest
import sqlalchemy as sa
from pydantic import (
    UUID1,
    UUID3,
    UUID4,
    UUID5,
    BaseModel,
    EmailStr,
    Field,
    IPvAnyAddress,
    IPvAnyInterface,
    IPvAnyNetwork,
    NameEmail,
    conbytes,
    condecimal,
    confloat,
    conint,
    constr,
)

from validatable.generic_types import GUID, Stringfy
from validatable.util import get_column


class CaseEnum(enum.Enum):
    a: int = 1
    b: int = 2
    c: str = "c"


class ModelCase(BaseModel):

    id: int = Field(sa_primary_key=True)
    python_uuid: uuid.UUID
    uuid1: UUID1
    uuid3: UUID3
    uuid4: UUID4
    uuid5: UUID5
    python_int: int = 1
    con_int: conint(strict=True)
    python_float: float = 1.23
    con_float: confloat(strict=True) = 1.23
    python_decimal: Decimal = 1.23
    con_decimal: condecimal(max_digits=10)
    python_str: str
    con_str: constr(max_length=10)
    email_str: EmailStr
    name_email: NameEmail
    python_bytes: bytes
    con_bytes: conbytes(max_length=10)
    python_path: pathlib.Path
    ipv4: IPv4Address
    ipv4i: IPv4Interface
    ipv4n: IPv4Network
    ipv6: IPv6Address
    ipv6i: IPv6Interface
    ipv6n: IPv6Network
    ipvany: IPvAnyAddress
    ipvanyi: IPvAnyInterface
    ipvanyn: IPvAnyNetwork
    dt_datetime: dt.datetime
    dt_date: dt.date
    dt_time: dt.time
    dt_timedelta: dt.timedelta
    enum_field: CaseEnum

    sa_type: Decimal = Field(sa_type=sa.DECIMAL(precision=10))
    sa_column: str = Field(
        sa_column=sa.Column(sa.String(255), nullable=False), max_length=255
    )


def test_get_column_python_int():
    """
    WHEN called with int
    THEN the SqlAlchemy type is BigInteger
    """
    field = ModelCase.__fields__.get("python_int")
    col = get_column(field)
    assert col.type.__class__ == sa.Integer


def test_get_column_con_int():
    """
    WHEN called with ConstrainedIntValue
    THEN the SqlAlchemy type is BigInteger
    """
    con_int = ModelCase.__fields__.get("con_int")
    col = get_column(con_int)
    assert col.type.__class__ == sa.Integer


def test_get_column_python_float():
    """
    WHEN called with float
    THEN the SqlAlchemy type is Float
    """
    python_float = ModelCase.__fields__.get("python_float")
    col = get_column(python_float)
    assert col.type.__class__ == sa.Float


def test_get_column_con_float():
    """
    WHEN called with ConstrainedFloatValue
    THEN the SqlAlchemy type is Float
    """
    con_float = ModelCase.__fields__.get("con_float")
    col = get_column(con_float)
    assert col.type.__class__ == sa.Float


def test_get_column_python_decimal():
    """
    WHEN called with Decimal
    THEN the SqlAlchemy type is Decimal
    """
    python_decimal = ModelCase.__fields__.get("python_decimal")
    col = get_column(python_decimal)
    assert col.type.__class__ == sa.Numeric


def test_get_column_con_decimal():
    """
    WHEN called with ConstrainedDecimalValue
    THEN the SqlAlchemy type is Decimal
    """
    con_decimal = ModelCase.__fields__.get("con_decimal")
    col = get_column(con_decimal)
    assert col.type.__class__ == sa.Numeric


def test_get_column_python_str():
    """
    WHEN called with str
    THEN the SqlAlchemy type is Text
    """
    python_str = ModelCase.__fields__.get("python_str")
    col = get_column(python_str)
    assert col.type.__class__ == Stringfy


def test_get_column_con_str():
    """
    WHEN called with ConstrainedStringValue with max_length=10
    THEN the SqlAlchemy type is String(10)
    """
    con_str = ModelCase.__fields__.get("con_str")
    col = get_column(con_str)
    assert col.type.__class__ == sa.String
    assert col.type.length == 10


def test_get_column_email_str():
    """
    WHEN called with ConstrainedStringValue with max_length=10
    THEN the SqlAlchemy type is String(10)
    """
    email_str = ModelCase.__fields__.get("email_str")
    col = get_column(email_str)
    assert col.type.__class__ == sa.String
    assert col.type.length == 320


def test_get_column_name_email():
    """
    WHEN called with ConstrainedStringValue with max_length=10
    THEN the SqlAlchemy type is String(10)
    """
    name_email = ModelCase.__fields__.get("name_email")
    col = get_column(name_email)
    assert col.type.__class__ == Stringfy


def test_get_column_python_bytes():
    """
    WHEN called with bytes
    THEN the SqlAlchemy type is LargeBinary
    """
    python_bytes = ModelCase.__fields__.get("python_bytes")
    col = get_column(python_bytes)
    assert col.type.__class__ == sa.LargeBinary


def test_get_column_con_bytes():
    """
    WHEN called with ConstrainedBytesValue
    THEN the SqlAlchemy type is LargeBinary
    """
    con_bytes = ModelCase.__fields__.get("con_bytes")
    col = get_column(con_bytes)
    assert col.type.__class__ == sa.LargeBinary


def test_get_column_python_path():
    """
    WHEN called with Path
    THEN the SqlAlchemy type is Text
    """
    python_path = ModelCase.__fields__.get("python_path")
    col = get_column(python_path)
    assert col.type.__class__ == Stringfy


def test_get_column_sa_col():
    """
    WHEN called with sa_col
    THEN the SqlAlchemy Column is returned
    """
    sa_column = ModelCase.__fields__.get("sa_column")
    col = get_column(sa_column)
    assert col.type.__class__ == sa.String
    assert col.type.length == 255
    assert not col.nullable


def test_get_column_sa_type():
    """
    WHEN called with sa_type
    THEN the SqlAlchemy Column with type is returned
    """
    sa_type = ModelCase.__fields__.get("sa_type")
    col = get_column(sa_type)
    assert col.type.__class__ == sa.DECIMAL
    assert col.type.precision == 10


@pytest.mark.parametrize(
    ("field", "length"),
    (
        (
            ("ipv4", 31),
            ("ipv4i", 31),
            ("ipv4n", 31),
            ("ipv6", 43),
            ("ipv6i", 43),
            ("ipv6n", 43),
            ("ipvany", 43),
            ("ipvanyi", 43),
            ("ipvanyn", 43),
        )
    ),
)
def test_get_column_network_types(field: str, length: int):
    """
    WHEN called with networktype
    THEN the SqlAlchemy type is String(length)
    """
    network_type = ModelCase.__fields__.get(field)
    col = get_column(network_type)
    assert col.type.__class__ == Stringfy


@pytest.mark.parametrize(
    ("field", "sa_type"),
    (
        ("dt_datetime", sa.DateTime),
        ("dt_date", sa.Date),
        ("dt_time", sa.Time),
        ("dt_timedelta", sa.Interval),
    ),
)
def test_get_column_datetimes(field: str, sa_type):
    """
    WHEN called with datetime types
    THEN get correct SqlAlchemy type
    """
    dt_field = ModelCase.__fields__.get(field)
    col = get_column(dt_field)
    assert col.type.__class__ == sa_type


def test_get_column_enum():
    """
    WHEN called with enum.Enum
    THEN returns correct SqlAlchemy type
    """
    field = ModelCase.__fields__.get("enum_field")
    col = get_column(field)
    assert col.type.__class__ == sa.Enum
    assert col.type.python_type == CaseEnum


@pytest.mark.parametrize(
    "field", ("python_uuid", "uuid1", "uuid3", "uuid4", "uuid5")
)
def test_get_column_uuid(field: str):
    """
    WHEN called with UUID
    THEN returns GUID
    """
    field = ModelCase.__fields__.get(field)
    col = get_column(field)
    assert col.type.__class__ == GUID
    assert col.type.python_type == uuid.UUID
