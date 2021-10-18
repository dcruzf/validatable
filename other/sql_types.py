from decimal import Decimal
from typing import Type

import sqlalchemy as sa
from pydantic.types import ConstrainedDecimal, ConstrainedInt


def String(
    length=None,
    collation=None,
    convert_unicode=False,
    unicode_error=None,
    _warn_on_bytestring=False,
    _expect_unicode=False,
) -> Type[str]:
    class StringModel(str):
        sa_type = sa.String(
            length=length,
            collation=collation,
            convert_unicode=convert_unicode,
            unicode_error=unicode_error,
            _warn_on_bytestring=_warn_on_bytestring,
            _expect_unicode=_expect_unicode,
        )

    return StringModel


def Integer(
    *,
    strict: bool = False,
    gt: int = None,
    ge: int = None,
    lt: int = None,
    le: int = None,
    multiple_of: int = None,
) -> Type[int]:
    # use kwargs then define conf in a dict to aid with IDE type hinting
    if not (gt and ge and lt and le):
        pass
    namespace = dict(
        strict=strict,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        multiple_of=multiple_of,
        sa_type_=sa.Integer,
    )
    return type("ConstrainedIntValue", (ConstrainedInt,), namespace)


def BigInt(
    *,
    strict: bool = False,
    gt: int = None,
    ge: int = None,
    lt: int = None,
    le: int = None,
    multiple_of: int = None,
) -> Type[int]:
    # use kwargs then define conf in a dict to aid with IDE type hinting
    namespace = dict(
        strict=strict,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        multiple_of=multiple_of,
        sa_type_=sa.BigInteger,
    )
    return type("ConstrainedIntValue", (ConstrainedInt,), namespace)


def SmallInteger(
    *,
    strict: bool = False,
    gt: int = None,
    ge: int = None,
    lt: int = None,
    le: int = None,
    multiple_of: int = None,
) -> Type[int]:
    # use kwargs then define conf in a dict to aid with IDE type hinting
    namespace = dict(
        strict=strict,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        multiple_of=multiple_of,
        sa_type_=sa.SmallInteger,
    )
    return type("ConstrainedIntValue", (ConstrainedInt,), namespace)


def Numeric(
    precision=None,
    scale=None,
    decimal_return_scale=None,
    asdecimal=True,
    *,
    gt: Decimal = None,
    ge: Decimal = None,
    lt: Decimal = None,
    le: Decimal = None,
    max_digits: int = None,
    decimal_places: int = None,
    multiple_of: Decimal = None,
) -> Type[Decimal]:
    # use kwargs then define conf in a dict to aid with IDE type hinting
    max_digits = max_digits or precision
    decimal_places = decimal_places or scale
    precision = precision or max_digits
    scale = scale or decimal_places
    namespace = dict(
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        max_digits=max_digits,
        decimal_places=decimal_places,
        multiple_of=multiple_of,
        sa_type_=sa.Numeric(
            precision=precision,
            scale=scale,
            decimal_return_scale=decimal_return_scale,
            asdecimal=asdecimal,
        ),
    )
    return type("ConstrainedDecimalValue", (ConstrainedDecimal,), namespace)
