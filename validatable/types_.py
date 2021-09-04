import re
from typing import Type

import sqlalchemy as sa
from pydantic.types import ConstrainedInt, ConstrainedStr, _registered


def String(
    length=None,
    collation=None,
    convert_unicode=False,
    unicode_error=None,
    _warn_on_bytestring=False,
    _expect_unicode=False,
    *,
    strip_whitespace: bool = False,
    to_lower: bool = False,
    strict: bool = False,
    min_length: int = None,
    max_length: int = None,
    curtail_length: int = None,
    regex: str = None,
) -> Type[str]:
    # use kwargs then define conf in a dict to aid with IDE type hinting

    namespace = dict(
        strip_whitespace=strip_whitespace,
        to_lower=to_lower,
        strict=strict,
        min_length=min_length,
        max_length=max_length,
        curtail_length=curtail_length,
        regex=regex and re.compile(regex),
        sa_type_=sa.String(
            length=length,
            collation=collation,
            convert_unicode=convert_unicode,
            unicode_error=unicode_error,
            _warn_on_bytestring=_warn_on_bytestring,
            _expect_unicode=_expect_unicode,
        ),
    )
    return _registered(
        type("ConstrainedStrValue", (ConstrainedStr,), namespace)
    )


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
