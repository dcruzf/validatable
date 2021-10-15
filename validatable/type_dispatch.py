import datetime as dt
import enum
import ipaddress
from decimal import Decimal
from pathlib import Path
from typing import Callable
from uuid import UUID
from weakref import WeakKeyDictionary, WeakSet

from pydantic import UUID1, UUID3, UUID4, UUID5
from pydantic.fields import ModelField
from pydantic.networks import (
    AnyHttpUrl,
    AnyUrl,
    EmailStr,
    HttpUrl,
    IPvAnyAddress,
    IPvAnyInterface,
    IPvAnyNetwork,
    NameEmail,
    pretty_email_regex,
)
from pydantic.types import (
    ConstrainedBytes,
    ConstrainedDecimal,
    ConstrainedFloat,
    ConstrainedInt,
    ConstrainedNumberMeta,
    ConstrainedStr,
    Json,
    JsonMeta,
    JsonWrapper,
    NegativeFloat,
    NegativeInt,
    NonNegativeFloat,
    NonNegativeInt,
    NonPositiveFloat,
    NonPositiveInt,
    PositiveFloat,
    PositiveInt,
    StrictBool,
    StrictFloat,
    StrictInt,
)
from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Enum,
    Float,
    Integer,
    Interval,
    LargeBinary,
    Numeric,
    SmallInteger,
    String,
    Time,
)

from .generic_types import GUID, AutoString, SLBigInteger


class Dispatch:
    def __init__(self, base: Callable):
        self._base = base
        self._funcs: WeakKeyDictionary = WeakKeyDictionary()

    def dispatcher(self, func: Callable):
        self._dispatcher = func

    def register(self, *args):
        self._types = WeakSet(args)
        return self.wrapper

    def wrapper(self, func):
        for t in self._types:
            self._funcs[t] = func
        self._types.clear()

    def __call__(self, *args, **kwargs):

        return self._dispatcher(*args, dispatch=self, **kwargs)


@Dispatch
def get_sql_type(m: ModelField, *args, **kwargs):
    raise TypeError(
        "cannot infer sqlalchemy "
        "type for {}-{}".format(m.type_, m.outer_type_)
    )


@get_sql_type.dispatcher
def _(m: ModelField, *args, dispatch: Dispatch = None, **kwargs):

    if m.outer_type_ in dispatch._funcs:
        func = dispatch._funcs.get(m.outer_type_)
        return func(m, *args, **kwargs)

    meta_func = dispatch._funcs.get(m.outer_type_.__class__)

    if meta_func:
        func = meta_func(m, dispatch=dispatch)
        if func:
            return func(m, *args, **kwargs)

    return dispatch._base(m)


@get_sql_type.register(  # type: ignore[no-redef]
    ConstrainedNumberMeta, JsonMeta, type
)
def _(m: ModelField, *args, dispatch: Dispatch = None, **kwargs):
    type_ = m.outer_type_
    if len(type_.__mro__) > 1 and type_.__mro__[1] in dispatch._funcs:
        return dispatch._funcs[type_.__mro__[1]]


@get_sql_type.register(enum.EnumMeta)  # type: ignore[no-redef]
def _(m: ModelField, *args, dispatch: Dispatch = None, **kwargs):
    return dispatch._funcs[enum.Enum]


@get_sql_type.register(str)  # type: ignore[no-redef]
def _(m: ModelField, *args, **kwargs):
    return AutoString


@get_sql_type.register(ConstrainedStr)  # type: ignore[no-redef]
def _(m: ModelField, *args, **kwargs):
    type_ = m.outer_type_
    length = type_.max_length or type_.curtail_length
    return String(length)


@get_sql_type.register(EmailStr)  # type: ignore[no-redef]
def _(m: ModelField, *args, **kwargs):
    return String(320)


@get_sql_type.register(NameEmail)  # type: ignore[no-redef]
def _(m: ModelField, *args, **kwargs):
    return AutoString(
        deserializer=lambda x: NameEmail(
            *pretty_email_regex.fullmatch(x).groups()
        )
    )


@get_sql_type.register(Path)  # type: ignore[no-redef]
def _(m: ModelField, *args, **kwargs):
    return AutoString(deserializer=Path)


@get_sql_type.register(  # type: ignore[no-redef]
    UUID, UUID1, UUID3, UUID4, UUID5
)
def _(m: ModelField, *args, **kwargs):
    return GUID


@get_sql_type.register(dt.datetime)  # type: ignore[no-redef]
def _(m: ModelField, *args, **kwargs):
    return DateTime


@get_sql_type.register(dt.date)  # type: ignore[no-redef]
def _(m: ModelField, *args, **kwargs):
    return Date


@get_sql_type.register(dt.time)  # type: ignore[no-redef]
def _(m: ModelField, *args, **kwargs):
    return Time


@get_sql_type.register(dt.timedelta)  # type: ignore[no-redef]
def _(m: ModelField, *args, **kwargs):
    return Interval


@get_sql_type.register(  # type: ignore[no-redef]
    IPvAnyAddress, ipaddress.IPv4Address, ipaddress.IPv6Address
)
def _(m: ModelField, *args, **kwargs):
    # https://datatracker.ietf.org/doc/html/rfc1924
    # IPv6 addresses, being 128 bits long, need 32 characters to write in
    # the general case, if standard hex representation, is used, plus more
    # for any punctuation inserted (typically about another 7 characters,
    # or 39 characters total).
    return AutoString(length=39, deserializer=ipaddress.ip_address)


@get_sql_type.register(  # type: ignore[no-redef]
    IPvAnyNetwork, ipaddress.IPv4Network, ipaddress.IPv6Network
)
def _(m: ModelField, *args, **kwargs):
    return AutoString(length=43, deserializer=ipaddress.ip_network)


@get_sql_type.register(  # type: ignore[no-redef]
    IPvAnyInterface, ipaddress.IPv4Interface, ipaddress.IPv6Interface
)
def _(m: ModelField, *args, **kwargs):
    return AutoString(length=43, deserializer=ipaddress.ip_interface)


@get_sql_type.register(HttpUrl)  # type: ignore[no-redef]
def _(m: ModelField, *args, **kwargs):
    return AutoString(length=HttpUrl.max_length)


@get_sql_type.register(AnyUrl, AnyHttpUrl)  # type: ignore[no-redef]
def _(m: ModelField, *args, **kwargs):

    return AutoString(length=AnyUrl.max_length)


@get_sql_type.register(  # type: ignore[no-redef]
    int,
    PositiveInt,
    NegativeInt,
    NonPositiveInt,
    NonNegativeInt,
    StrictInt,
)
def _(m: ModelField, *args, **kwargs):
    # https://docs.sqlalchemy.org/en/14/dialects/sqlite.html
    return SLBigInteger


@get_sql_type.register(ConstrainedInt)  # type: ignore[no-redef]
def _(m: ModelField, *args, **kwargs):
    type_ = m.outer_type_
    min_value = type_.gt or type_.ge
    max_value = type_.lt or type_.le
    if not (min_value and max_value):
        return BigInteger

    if min_value >= -32768 and max_value <= 32767:
        return SmallInteger

    if min_value >= -2147483648 and max_value <= 2147483647:
        return Integer

    return BigInteger


@get_sql_type.register(  # type: ignore[no-redef]
    float,
    ConstrainedFloat,
    PositiveFloat,
    NegativeFloat,
    NonPositiveFloat,
    NonNegativeFloat,
    StrictFloat,
)
def _(m: ModelField, *args, **kwargs):

    return Float


@get_sql_type.register(Decimal)  # type: ignore[no-redef]
def _(m: ModelField, *args, **kwargs):

    return Numeric


@get_sql_type.register(ConstrainedDecimal)  # type: ignore[no-redef]
def _(m: ModelField, *args, **kwargs):
    type_ = m.outer_type_
    return Numeric(precision=type_.max_digits, scale=type_.decimal_places)


@get_sql_type.register(bytes)  # type: ignore[no-redef]
def _(m: ModelField, *args, **kwargs):
    return LargeBinary


@get_sql_type.register(ConstrainedBytes)  # type: ignore[no-redef]
def _(m: ModelField, *args, **kwargs):
    type_ = m.outer_type_
    if type_.max_length:
        return LargeBinary(type_.max_length)
    return LargeBinary


@get_sql_type.register(enum.Enum)  # type: ignore[no-redef]
def _(m: ModelField, *args, **kwargs):
    type_ = m.outer_type_

    return Enum(type_)


@get_sql_type.register(JsonWrapper, Json)  # type: ignore[no-redef]
def _(m: ModelField, *args, **kwargs):
    return JSON


@get_sql_type.register(bool, StrictBool)  # type: ignore[no-redef]
def _(m: ModelField, *args, **kwargs):
    return Boolean
