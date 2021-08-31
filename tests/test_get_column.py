import pathlib
from decimal import Decimal

import sqlalchemy as sa
from pydantic import (
    BaseModel,
    Field,
    conbytes,
    condecimal,
    confloat,
    conint,
    constr,
)

from validatable.util import get_column


class ModelCase(BaseModel):

    id: int = Field(sa_primary_key=True)
    python_int: int = 1
    con_int: conint(strict=True)
    python_float: float = 1.23
    con_float: confloat(strict=True) = 1.23
    python_decimal: Decimal = 1.23
    con_decimal: condecimal(max_digits=10)
    python_str: str
    con_str: constr(max_length=10)
    python_bytes: bytes
    con_bytes: conbytes(max_length=10)
    python_path: pathlib.Path
    sa_type: str = Field(sa_type=sa.DECIMAL(precision=10))
    sa_col: str = Field(
        sa_col=sa.Column(sa.String(255), nullable=False), max_length=255
    )


def test_get_column_python_int():
    """
    WHEN called with int
    THEN the SqlAlchemy type is BigInteger
    """
    python_int = ModelCase.__fields__.get("python_int")
    col = get_column(python_int)
    assert col.type.__class__ == sa.BigInteger


def test_get_column_con_int():
    """
    WHEN called with ConstrainedIntValue
    THEN the SqlAlchemy type is BigInteger
    """
    con_int = ModelCase.__fields__.get("con_int")
    col = get_column(con_int)
    assert col.type.__class__ == sa.BigInteger


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
    assert col.type.__class__ == sa.Text


def test_get_column_con_str():
    """
    WHEN called with ConstrainedStringValue with max_length=10
    THEN the SqlAlchemy type is String(10)
    """
    con_str = ModelCase.__fields__.get("con_str")
    col = get_column(con_str)
    assert col.type.__class__ == sa.String
    assert col.type.length == 10


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
    assert col.type.__class__ == sa.Text


def test_get_column_sa_col():
    """
    WHEN called with sa_col
    THEN the SqlAlchemy Column is returned
    """
    sa_col = ModelCase.__fields__.get("sa_col")
    col = get_column(sa_col)
    assert col.type.__class__ == sa.String
    assert col.type.length == 255


def test_get_column_sa_type():
    """
    WHEN called with sa_type
    THEN the SqlAlchemy Column with type is returned
    """
    sa_col = ModelCase.__fields__.get("sa_col")
    col = get_column(sa_col)
    assert col.type.__class__ == sa.String
    assert col.type.length == 255
