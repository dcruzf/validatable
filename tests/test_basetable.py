import datetime as dt
import enum
import pathlib
import random
import uuid
from decimal import Decimal
from ipaddress import (
    IPv4Address,
    IPv4Interface,
    IPv4Network,
    IPv6Address,
    IPv6Interface,
    IPv6Network,
    ip_address,
    ip_interface,
    ip_network,
)

import pytest
import sqlalchemy as sa
from faker import Faker
from pydantic import (
    UUID1,
    UUID3,
    UUID4,
    UUID5,
    EmailStr,
    Field,
    IPvAnyAddress,
    IPvAnyInterface,
    IPvAnyNetwork,
    NameEmail,
    NegativeFloat,
    NegativeInt,
    PositiveFloat,
    PositiveInt,
    conbytes,
    condecimal,
    confloat,
    conint,
    constr,
)

from validatable.main import BaseTable

Faker.seed(2)
faker = Faker()


NUM_TEST: int = 10
engine = sa.create_engine("sqlite:///:memory:")

metadata = sa.MetaData()


@pytest.fixture
def conn():
    with engine.connect() as conn:
        metadata.create_all(engine)
        yield conn
        metadata.drop_all(engine)


class ModelCaseUUID(BaseTable, metadata=metadata):
    id: UUID4 = Field(default_factory=uuid.uuid4, sa_primary_key=True)
    uuid1: UUID1 = Field(default_factory=uuid.uuid1)
    uuid3: UUID3 = Field(
        default_factory=lambda: uuid.uuid3(uuid.uuid4(), "name")
    )
    uuid4: UUID4 = Field(default_factory=uuid.uuid4)
    uuid5: UUID5 = Field(
        default_factory=lambda: uuid.uuid5(uuid.uuid4(), "name")
    )


class ModelCaseNumber(BaseTable, metadata=metadata):
    id: UUID4 = Field(default_factory=uuid.uuid4, sa_primary_key=True)
    python_int: int = Field(
        default_factory=lambda: random.randint(-2147483648, 2147483647)
    )
    con_int: conint() = Field(
        default_factory=lambda: random.randint(-2147483648, 2147483647)
    )
    python_float: float = Field(
        default_factory=lambda: random.uniform(
            -3.402823466e38, 1.175494351e-38
        )
    )
    con_float: confloat() = Field(
        default_factory=lambda: random.uniform(
            -3.402823466e38, 1.175494351e-38
        )
    )
    python_decimal: Decimal = Field(
        default_factory=lambda: f"{random.uniform(-1000000000, 1000000000):.10f}"  # noqa E501
    )
    con_decimal: condecimal() = Field(
        default_factory=lambda: f"{random.uniform(-1000000000, 1000000000):.10f}"  # noqa E501
    )
    pint: PositiveInt = Field(
        default_factory=lambda: random.randint(0, 2147483647)
    )
    nint: NegativeInt = Field(
        default_factory=lambda: random.randint(-2147483648, 0)
    )
    pfloat: PositiveFloat = Field(
        default_factory=lambda: random.uniform(0, 1.175494351e-38)
    )
    nfloat: NegativeFloat = Field(
        default_factory=lambda: random.uniform(-3.402823466e38, 0)
    )


class ModelCaseStrBytes(BaseTable, metadata=metadata):
    id: UUID4 = Field(default_factory=uuid.uuid4, sa_primary_key=True)
    python_str: str = Field(
        default_factory=faker.sentence, sa_primary_key=True
    )
    con_str: constr(max_length=10) = Field(
        default_factory=lambda: f"{faker.sentence()}"[:10]
    )
    email_str: EmailStr = Field(default_factory=faker.email)

    # NameEmail do not allow points "." in validation. Example: 'Mr.', 'Jr.'
    # https://github.com/samuelcolvin/pydantic/issues/2955
    name_email: NameEmail = Field(
        default_factory=lambda: NameEmail(
            name=faker.name().replace(".", ""), email=faker.email()
        )
    )
    python_path: pathlib.Path = Field(
        default_factory=lambda: pathlib.PosixPath(
            faker.file_path(depth=random.randint(1, 5))
        )
    )
    python_bytes: bytes = Field(default_factory=lambda: random.randbytes(10))
    con_bytes: conbytes(max_length=10) = Field(
        default_factory=lambda: random.randbytes(10)
    )


class ModelCaseNetwork(BaseTable, metadata=metadata):
    id: UUID4 = Field(default_factory=uuid.uuid4, sa_primary_key=True)
    ipv4: IPv4Address = Field(default_factory=lambda: ip_address(faker.ipv4()))
    ipv4i: IPv4Interface = Field(
        default_factory=lambda: ip_interface(faker.ipv4(network=True))
    )
    ipv4n: IPv4Network = Field(
        default_factory=lambda: ip_network(faker.ipv4(network=True))
    )
    ipv6: IPv6Address = Field(default_factory=lambda: ip_address(faker.ipv6()))
    ipv6i: IPv6Interface = Field(
        default_factory=lambda: ip_interface(faker.ipv6(network=True))
    )
    ipv6n: IPv6Network = Field(
        default_factory=lambda: ip_network(faker.ipv6(network=True))
    )
    ipvany: IPvAnyAddress = Field(
        default_factory=lambda: ip_address(
            faker.ipv6() if random.choice([True, False]) else faker.ipv4()
        )
    )
    ipvanyi: IPvAnyInterface = Field(
        default_factory=lambda: ip_interface(
            faker.ipv6(network=True)
            if random.choice([True, False])
            else faker.ipv4(network=True)
        )
    )
    ipvanyn: IPvAnyNetwork = Field(
        default_factory=lambda: ip_network(
            faker.ipv6(network=True)
            if random.choice([True, False])
            else faker.ipv4(network=True)
        )
    )


class ModelCaseDateTime(BaseTable, metadata=metadata):
    id: UUID4 = Field(default_factory=uuid.uuid4, sa_primary_key=True)
    dt_datetime: dt.datetime = Field(default_factory=faker.date_time_between)
    dt_date: dt.date = Field(default_factory=faker.date_between)
    dt_time: dt.time = Field(default_factory=faker.time_object)
    dt_timedelta: dt.timedelta = Field(
        default_factory=lambda: dt.timedelta(
            microseconds=random.randint(0, 999999999)
        )
    )


class CaseEnum(enum.Enum):
    a: int = 1
    b: int = 2
    c: int = 3


class ModelCaseEnum(BaseTable, metadata=metadata):
    id: UUID4 = Field(default_factory=uuid.uuid4, sa_primary_key=True)
    enum_field: CaseEnum = Field(
        default_factory=lambda: getattr(
            CaseEnum, random.choice(list(CaseEnum.__members__.keys()))
        )
    )


def test_table_declaration():

    table = sa.Table(
        "modelcase",
        metadata,
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    )

    class ModelCase(BaseTable):

        __sa_table__ = table
        id: int = None

    assert table == ModelCase.__sa_table__


def test_raise_for_wrong_metadata():

    with pytest.raises(TypeError):

        class ModelCase(BaseTable, metadata="NotMetaData"):
            id: int = None


@pytest.mark.parametrize("model", [ModelCaseUUID() for n in range(NUM_TEST)])
def test_database_uuid(model: ModelCaseUUID, conn):
    query = model.__sa_table__.insert().values(model.dict())
    one = model.__sa_table__.select().where(
        model.__sa_table__.c.id == model.id
    )

    conn.execute(query)
    result = conn.execute(one)
    data = result.fetchone()

    m = ModelCaseUUID.parse_obj(data)
    assert m == model


@pytest.mark.parametrize("model", [ModelCaseNumber() for n in range(NUM_TEST)])
def test_database_number(model: ModelCaseNumber, conn):

    query = model.__sa_table__.insert().values(model.dict())
    one = model.__sa_table__.select().where(
        model.__sa_table__.c.id == model.id
    )

    conn.execute(query)
    result = conn.execute(one)
    data = result.fetchone()

    m = ModelCaseNumber.parse_obj(data)

    # Dialect sqlite+pysqlite does *not* support Decimal objects natively
    if engine.name == "sqlite":
        assert m.dict(exclude={"python_decimal", "con_decimal"}) == model.dict(
            exclude={"python_decimal", "con_decimal"}
        )
        assert (float(m.con_decimal) - float(model.con_decimal)) < 0.001
        assert (float(m.python_decimal) - float(model.python_decimal)) < 0.001
    else:
        assert m == model


@pytest.mark.parametrize(
    "model", [ModelCaseStrBytes() for n in range(NUM_TEST)]
)
def test_database_strbytes(model: ModelCaseStrBytes, conn):

    query = model.__sa_table__.insert().values(model.dict())
    one = model.__sa_table__.select().where(
        model.__sa_table__.c.id == model.id
    )

    conn.execute(query)
    result = conn.execute(one)
    data = result.fetchone()

    m = ModelCaseStrBytes.parse_obj(data)

    assert m == model


@pytest.mark.parametrize(
    "model", [ModelCaseNetwork() for n in range(NUM_TEST)]
)
def test_database_network(model: ModelCaseNetwork, conn):

    query = model.__sa_table__.insert().values(model.dict())
    one = model.__sa_table__.select().where(
        model.__sa_table__.c.id == model.id
    )

    conn.execute(query)
    result = conn.execute(one)
    data = result.fetchone()

    m = ModelCaseNetwork.parse_obj(data)

    assert m == model


@pytest.mark.parametrize(
    "model", [ModelCaseDateTime() for n in range(NUM_TEST)]
)
def test_database_datetime(model: ModelCaseDateTime, conn):

    query = model.__sa_table__.insert().values(model.dict())
    one = model.__sa_table__.select().where(
        model.__sa_table__.c.id == model.id
    )

    conn.execute(query)
    result = conn.execute(one)
    data = result.fetchone()

    m = ModelCaseDateTime.parse_obj(data)

    assert m == model


@pytest.mark.parametrize("model", [ModelCaseEnum() for n in range(NUM_TEST)])
def test_database_enum(model: ModelCaseEnum, conn):

    query = model.__sa_table__.insert().values(model.dict())
    one = model.__sa_table__.select().where(
        model.__sa_table__.c.id == model.id
    )

    conn.execute(query)
    result = conn.execute(one)
    data = result.fetchone()

    m = ModelCaseEnum.parse_obj(data)

    assert m == model
