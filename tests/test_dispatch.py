<<<<<<< HEAD
import enum
import uuid
from decimal import Decimal
from typing import Dict, Optional

import pytest
from pydantic import (
    UUID1,
    UUID3,
    UUID4,
    UUID5,
    BaseModel,
    ConstrainedDecimal,
    ConstrainedFloat,
    ConstrainedInt,
    NegativeFloat,
    NegativeInt,
    NonNegativeFloat,
    NonNegativeInt,
    NonPositiveFloat,
    NonPositiveInt,
    PositiveFloat,
    PositiveInt,
    StrictFloat,
    StrictInt,
    condecimal,
    conint,
)
from pydantic.fields import ModelField
from pydantic.types import ConstrainedNumberMeta, JsonMeta

from validatable.type_dispatch import Dispatch, get_sql_type


class CaseEnum(enum.Enum):
    a: int = 1
    b: int = 2
    c: str = "c"


MAX_LENGTH: int = 10


class ModelCaseInt(BaseModel):

    python_int: int
    con_int: conint()  # type: ignore
    ccon_int: ConstrainedInt
    p_int: PositiveInt
    n_int: NegativeInt
    np_int: NonPositiveInt
    nn_int: NonNegativeInt
    s_int: StrictInt
    opython_int: Optional[int]
    ocon_int: Optional[conint()]  # type: ignore
    occon_int: Optional[ConstrainedInt]
    op_int: Optional[PositiveInt]
    on_int: Optional[NegativeInt]
    onp_int: Optional[NonPositiveInt]
    onn_int: Optional[NonNegativeInt]
    os_int: Optional[StrictInt]


class ModelCaseFloat(BaseModel):

    python_float: ConstrainedFloat
    p_float: PositiveFloat
    n_float: NegativeFloat
    np_float: NonPositiveFloat
    nn_float: NonNegativeFloat
    s_float: StrictFloat
    opython_float: Optional[ConstrainedFloat]
    op_float: Optional[PositiveFloat]
    on_float: Optional[NegativeFloat]
    onp_float: Optional[NonPositiveFloat]
    onn_float: Optional[NonNegativeFloat]
    os_float: Optional[StrictFloat]


class ModelCaseUUID(BaseModel):

    python_uuid: uuid.UUID
    uuid1: UUID1
    uuid3: UUID3
    uuid4: UUID4
    uuid5: UUID5
    opython_uuid: Optional[uuid.UUID]
    ouuid1: Optional[UUID1]
    ouuid3: Optional[UUID3]
    ouuid4: Optional[UUID4]
    ouuid5: Optional[UUID5]


class ModelCaseDecimal(BaseModel):
    python_decimal: Decimal
    con_decimal: condecimal(max_digits=10)  # type: ignore
    c_decimal: ConstrainedDecimal
    opython_decimal: Optional[Decimal]
    ocon_decimal: Optional[condecimal(max_digits=10)]  # type: ignore
    oc_decimal: Optional[ConstrainedDecimal]


class ModelCaseTypes(
    ModelCaseUUID, ModelCaseFloat, ModelCaseInt, ModelCaseDecimal
):
    ...


@pytest.fixture(scope="function")
def dispatch():
    @Dispatch
    def dispatch(m, *args, **kwargs):
        raise TypeError(f"Oh, No! {m.type_}, {m.outer_type_}")

    @dispatch.dispatcher
    def _(m: ModelField, *args, dispatch: Dispatch = None, **kwargs):

        if m.outer_type_ in dispatch._funcs:
            func = dispatch._funcs.get(m.outer_type_)
            return func(m, *args, **kwargs)

        meta_func = dispatch._funcs.get(m.outer_type_.__class__)

        if meta_func is None:
            return dispatch._base(m)
        else:
            func = meta_func(m, dispatch=dispatch)
            return func(m, *args, **kwargs)

    @dispatch.register(ConstrainedNumberMeta, JsonMeta, type)
    def _(m: ModelField, *args, dispatch: Dispatch = None, **kwargs):
        type_ = m.outer_type_
        if type_.__mro__[1] in dispatch._funcs:
            return dispatch._funcs[type_.__mro__[1]]

    yield dispatch


@pytest.mark.parametrize(
    "field",
    ModelCaseUUID.__fields__.values(),
    ids=ModelCaseUUID.__fields__.keys(),
)
def test_dispatch_uuid(field, dispatch):
    m = field

    @dispatch.register(uuid.UUID, UUID1, UUID3, UUID4, UUID5)
    def _(m):
        return "uuid"

    assert dispatch(m) == "uuid"


@pytest.mark.parametrize(
    "field",
    ModelCaseInt.__fields__.values(),
    ids=ModelCaseInt.__fields__.keys(),
)
def test_dispatch_int(field, dispatch):
    m = field

    @dispatch.register(
        int,
        PositiveInt,
        NegativeInt,
        NonPositiveInt,
        NonNegativeInt,
        StrictInt,
        ConstrainedInt,
    )
    def _(m):
        return "int"

    assert dispatch(m) == "int"


@pytest.mark.parametrize(
    "field",
    ModelCaseFloat.__fields__.values(),
    ids=ModelCaseFloat.__fields__.keys(),
)
def test_dispatch_float(field, dispatch):
    m = field

    @dispatch.register(
        float,
        ConstrainedFloat,
        PositiveFloat,
        NegativeFloat,
        NonPositiveFloat,
        NonNegativeFloat,
        StrictFloat,
    )
    def _(m):
        return "float"

    assert dispatch(m) == "float"


@pytest.mark.parametrize(
    "field",
    ModelCaseDecimal.__fields__.values(),
    ids=ModelCaseDecimal.__fields__.keys(),
)
def test_dispatch_decimal(field, dispatch):
    m = field

    @dispatch.register(
        Decimal,
        ConstrainedDecimal,
    )
    def _(m):
        return "decimal"

    assert dispatch(m) == "decimal"


@pytest.mark.parametrize(
    ("key", "field"),
    ModelCaseTypes.__fields__.items(),
    ids=ModelCaseTypes.__fields__.keys(),
)
def test_dispatch_types(field, key, dispatch):
    m = field

    @dispatch.register(uuid.UUID, UUID1, UUID3, UUID4, UUID5)
    def _(m):
        return "uuid"

    @dispatch.register(
        float,
        ConstrainedFloat,
        PositiveFloat,
        NegativeFloat,
        NonPositiveFloat,
        NonNegativeFloat,
        StrictFloat,
    )
    def _(m):
        return "float"

    @dispatch.register(
        int,
        PositiveInt,
        NegativeInt,
        NonPositiveInt,
        NonNegativeInt,
        StrictInt,
        ConstrainedInt,
    )
    def _(m):
        return "int"

    @dispatch.register(
        Decimal,
        ConstrainedDecimal,
    )
    def _(m):
        return "decimal"

    assert dispatch(m) in key


def test_wrong_type():
    class BaseWrong(BaseModel):
        test: Dict

    with pytest.raises(TypeError):
        get_sql_type(BaseWrong.__fields__["test"])
||||||| constructed merge base
=======
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
from typing import Optional

import pytest
import sqlalchemy as sa
from pydantic import (
    UUID1,
    UUID3,
    UUID4,
    UUID5,
    BaseModel,
    ConstrainedDecimal,
    ConstrainedFloat,
    ConstrainedInt,
    EmailStr,
    Field,
    IPvAnyAddress,
    IPvAnyInterface,
    IPvAnyNetwork,
    NameEmail,
    NegativeFloat,
    NegativeInt,
    NonNegativeFloat,
    NonNegativeInt,
    NonPositiveFloat,
    NonPositiveInt,
    PositiveFloat,
    PositiveInt,
    StrictFloat,
    StrictInt,
    conbytes,
    condecimal,
    confloat,
    conint,
    constr,
)
from pydantic.fields import ModelField
from pydantic.types import ConstrainedNumberMeta, JsonMeta

from validatable.type_dispatch import Dispatch


class CaseEnum(enum.Enum):
    a: int = 1
    b: int = 2
    c: str = "c"


MAX_LENGTH: int = 10


class ModelCaseInt(BaseModel):

    python_int: int
    con_int: conint()  # type: ignore
    ccon_int: ConstrainedInt
    p_int: PositiveInt
    n_int: NegativeInt
    np_int: NonPositiveInt
    nn_int: NonNegativeInt
    s_int: StrictInt
    opython_int: Optional[int]
    ocon_int: Optional[conint()]  # type: ignore
    occon_int: Optional[ConstrainedInt]
    op_int: Optional[PositiveInt]
    on_int: Optional[NegativeInt]
    onp_int: Optional[NonPositiveInt]
    onn_int: Optional[NonNegativeInt]
    os_int: Optional[StrictInt]


class ModelCaseFloat(BaseModel):

    python_float: ConstrainedFloat
    p_float: PositiveFloat
    n_float: NegativeFloat
    np_float: NonPositiveFloat
    nn_float: NonNegativeFloat
    s_float: StrictFloat
    opython_float: Optional[ConstrainedFloat]
    op_float: Optional[PositiveFloat]
    on_float: Optional[NegativeFloat]
    onp_float: Optional[NonPositiveFloat]
    onn_float: Optional[NonNegativeFloat]
    os_float: Optional[StrictFloat]


class ModelCaseUUID(BaseModel):

    python_uuid: uuid.UUID
    uuid1: UUID1
    uuid3: UUID3
    uuid4: UUID4
    uuid5: UUID5
    opython_uuid: Optional[uuid.UUID]
    ouuid1: Optional[UUID1]
    ouuid3: Optional[UUID3]
    ouuid4: Optional[UUID4]
    ouuid5: Optional[UUID5]


class ModelCaseDecimal(BaseModel):
    python_decimal: Decimal
    con_decimal: condecimal(max_digits=10)  # type: ignore
    c_decimal: ConstrainedDecimal
    opython_decimal: Optional[Decimal]
    ocon_decimal: Optional[condecimal(max_digits=10)]  # type: ignore
    oc_decimal: Optional[ConstrainedDecimal]


class ModelCaseTypes(
    ModelCaseUUID, ModelCaseFloat, ModelCaseInt, ModelCaseDecimal
):
    ...


class ModelCase(BaseModel):

    python_uuid: uuid.UUID
    uuid1: UUID1
    uuid3: UUID3
    uuid4: UUID4
    uuid5: UUID5
    python_int: int
    con_int: conint(strict=True)  # type: ignore
    python_float: float
    con_float: confloat(strict=True)  # type: ignore
    python_decimal: Decimal
    con_decimal: condecimal(max_digits=10)  # type: ignore
    python_str: str
    python_str_max: str = Field(max_length=MAX_LENGTH)
    con_str: constr(max_length=MAX_LENGTH)  # type: ignore
    con_str_curtain: constr(curtail_length=MAX_LENGTH)  # type: ignore
    con_str_curtain_max: constr(  # type: ignore
        curtail_length=MAX_LENGTH, max_length=2 * MAX_LENGTH
    )
    email_str: EmailStr
    name_email: NameEmail
    python_bytes: bytes
    python_bytes_max: bytes = Field(max_length=MAX_LENGTH)
    con_bytes: conbytes(max_length=MAX_LENGTH)  # type: ignore
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
    name: int = Field(sa_column=sa.Column("not_valid", sa.Integer))

    sa_type: Decimal = Field(sa_type=sa.DECIMAL(precision=10))
    sa_column: str = Field(
        sa_column=sa.Column(sa.String(255), nullable=False), max_length=255
    )


@pytest.fixture(scope="function")
def dispatch():
    @Dispatch
    def dispatch(m, *args, **kwargs):
        raise TypeError(f"Oh, No! {m.type_}, {m.outer_type_}")

    @dispatch.dispatcher
    def _(m: ModelField, *args, dispatch: Dispatch = None, **kwargs):

        if m.outer_type_ in dispatch._funcs:
            func = dispatch._funcs.get(m.outer_type_)
            return func(m, *args, **kwargs)

        meta_func = dispatch._funcs.get(m.outer_type_.__class__)

        if meta_func is None:
            return dispatch._base(m)
        else:
            func = meta_func(m, dispatch=dispatch)
            return func(m, *args, **kwargs)

    @dispatch.register(ConstrainedNumberMeta, JsonMeta, type)
    def _(m: ModelField, *args, dispatch: Dispatch = None, **kwargs):
        type_ = m.outer_type_
        if type_.__mro__[1] in dispatch._funcs:
            return dispatch._funcs[type_.__mro__[1]]

    yield dispatch


@pytest.mark.parametrize(
    "field",
    ModelCaseUUID.__fields__.values(),
    ids=ModelCaseUUID.__fields__.keys(),
)
def test_dispatch_uuid(field, dispatch):
    m = field

    @dispatch.register(uuid.UUID, UUID1, UUID3, UUID4, UUID5)
    def _(m):
        return "uuid"

    assert dispatch(m) == "uuid"


@pytest.mark.parametrize(
    "field",
    ModelCaseInt.__fields__.values(),
    ids=ModelCaseInt.__fields__.keys(),
)
def test_dispatch_int(field, dispatch):
    m = field

    @dispatch.register(
        int,
        PositiveInt,
        NegativeInt,
        NonPositiveInt,
        NonNegativeInt,
        StrictInt,
        ConstrainedInt,
    )
    def _(m):
        return "int"

    assert dispatch(m) == "int"


@pytest.mark.parametrize(
    "field",
    ModelCaseFloat.__fields__.values(),
    ids=ModelCaseFloat.__fields__.keys(),
)
def test_dispatch_float(field, dispatch):
    m = field

    @dispatch.register(
        float,
        ConstrainedFloat,
        PositiveFloat,
        NegativeFloat,
        NonPositiveFloat,
        NonNegativeFloat,
        StrictFloat,
    )
    def _(m):
        return "float"

    assert dispatch(m) == "float"


@pytest.mark.parametrize(
    "field",
    ModelCaseDecimal.__fields__.values(),
    ids=ModelCaseDecimal.__fields__.keys(),
)
def test_dispatch_decimal(field, dispatch):
    m = field

    @dispatch.register(
        Decimal,
        ConstrainedDecimal,
    )
    def _(m):
        return "decimal"

    assert dispatch(m) == "decimal"


@pytest.mark.parametrize(
    ("key", "field"),
    ModelCaseTypes.__fields__.items(),
    ids=ModelCaseTypes.__fields__.keys(),
)
def test_dispatch_types(field, key, dispatch):
    m = field

    @dispatch.register(uuid.UUID, UUID1, UUID3, UUID4, UUID5)
    def _(m):
        return "uuid"

    @dispatch.register(
        float,
        ConstrainedFloat,
        PositiveFloat,
        NegativeFloat,
        NonPositiveFloat,
        NonNegativeFloat,
        StrictFloat,
    )
    def _(m):
        return "float"

    @dispatch.register(
        int,
        PositiveInt,
        NegativeInt,
        NonPositiveInt,
        NonNegativeInt,
        StrictInt,
        ConstrainedInt,
    )
    def _(m):
        return "int"

    @dispatch.register(
        Decimal,
        ConstrainedDecimal,
    )
    def _(m):
        return "decimal"

    assert dispatch(m) in key
>>>>>>> 🔥 Added support for new types: AnyUrl, HttpAnyUrl, HttpUrl, StrictUrl, bool and StrictBool (#42)
