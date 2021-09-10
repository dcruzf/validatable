import datetime as dt
import enum
import os
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


NUM_TEST = int(os.getenv("N") or 1)
DATABASE = os.getenv("DB") or "sqlite"
metadata = sa.MetaData()


@pytest.fixture(scope="session")
def engine():

    if DATABASE == "sqlite":
        yield sa.create_engine("sqlite:///:memory:")
    if DATABASE == "postgresql":
        yield sa.create_engine(
            "postgresql://validatable:password@localhost:5432/db"
        )
    if DATABASE == "mariadb":
        yield sa.create_engine(
            "mariadb://validatable:password@localhost:3306/db"
        )


@pytest.fixture(scope="function")
def conn(engine):
    metadata.create_all(engine)
    with engine.connect() as conn:
        yield conn
    metadata.drop_all(engine)


class Base(BaseTable):
    id: UUID4 = Field(default_factory=uuid.uuid4, sa_primary_key=True)
    metadata = metadata


class ModelCaseUUID(Base):
    uuid1: UUID1 = Field(default_factory=uuid.uuid1)
    uuid3: UUID3 = Field(
        default_factory=lambda: uuid.uuid3(uuid.uuid4(), "name")
    )
    uuid4: UUID4 = Field(default_factory=uuid.uuid4)
    uuid5: UUID5 = Field(
        default_factory=lambda: uuid.uuid5(uuid.uuid4(), "name")
    )


class ModelCaseNumber(Base):
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
        default_factory=lambda: Decimal(
            f"{random.uniform(-1000000000, 1000000000):.10f}"
        )  # noqa E501
    )
    con_decimal: condecimal() = Field(
        default_factory=lambda: Decimal(
            f"{random.uniform(-1000000000, 1000000000):.10f}"
        )  # noqa E501
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


class ModelCaseStrBytes(Base):
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


class ModelCaseNetwork(Base):
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


class ModelCaseDateTime(Base):
    dt_datetime: dt.datetime = Field(default_factory=faker.date_time_between)
    dt_date: dt.date = Field(default_factory=faker.date_between)
    dt_time: dt.time = Field(default_factory=faker.time_object)
    dt_timedelta: dt.timedelta = Field(
        default_factory=lambda: dt.timedelta(
            microseconds=random.randint(0, 999999999)
        )
    )


class CaseEnum(enum.Enum):
    a: int = "a"
    b: int = "b"
    c: int = "c"


class CaseIntEnum(enum.IntEnum):
    a: int = 1
    b: int = 2
    c: int = 3


class ModelCaseEnum(Base):
    enum_field: CaseEnum = Field(
        default_factory=lambda: getattr(
            CaseEnum, random.choice(list(CaseEnum.__members__.keys()))
        )
    )
    int_enum_field: CaseEnum = Field(
        default_factory=lambda: getattr(
            CaseEnum, random.choice(list(CaseIntEnum.__members__.keys()))
        )
    )


class ModelUpdateDelete(BaseTable, metadata=metadata):
    id: UUID4 = Field(default_factory=uuid.uuid4, sa_primary_key=True)
    num: int = 0


def test_metadata_property():

    meta = sa.MetaData()

    class ModelCase(BaseTable, metadata=meta):
        id: int = Field(sa_primary_key=True)

    class Base(BaseTable):
        metadata = meta
        id: int = Field(sa_primary_key=True)

    class TableFromBase(Base):
        ...

    class Table(BaseTable):
        __sa_metadata__ = meta
        id: int = Field(sa_primary_key=True)

    assert TableFromBase.metadata == meta
    assert ModelCase.metadata == meta
    assert Table.metadata == meta


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
    insert = ModelCaseUUID.insert().values(model.dict())
    one = ModelCaseUUID.select().where(ModelCaseUUID.c.id == model.id)

    conn.execute(insert)
    result = conn.execute(one)
    data = result.fetchone()

    m = ModelCaseUUID.parse_obj(data)
    assert m == model


@pytest.mark.filterwarnings(
    r"ignore:Dialect sqlite\+pysqlite does \*not\* "
    r"support Decimal objects natively"
)
@pytest.mark.parametrize("model", [ModelCaseNumber() for n in range(NUM_TEST)])
def test_database_number(model: ModelCaseNumber, conn):

    insert = ModelCaseNumber.insert().values(model.dict())
    one = ModelCaseNumber.select().where(ModelCaseNumber.c.id == model.id)

    conn.execute(insert)
    result = conn.execute(one)
    data = result.fetchone()

    m = ModelCaseNumber.parse_obj(data)

    assert m == model


@pytest.mark.parametrize(
    "model", [ModelCaseStrBytes() for n in range(NUM_TEST)]
)
def test_database_strbytes(model: ModelCaseStrBytes, conn):

    insert = ModelCaseStrBytes.insert().values(model.dict())
    one = ModelCaseStrBytes.select().where(ModelCaseStrBytes.c.id == model.id)

    conn.execute(insert)
    result = conn.execute(one)
    data = result.fetchone()

    m = ModelCaseStrBytes.parse_obj(data)

    assert m == model


@pytest.mark.parametrize(
    "model", [ModelCaseNetwork() for n in range(NUM_TEST)]
)
def test_database_network(model: ModelCaseNetwork, conn):

    insert = ModelCaseNetwork.insert().values(model.dict())
    one = ModelCaseNetwork.select().where(ModelCaseNetwork.c.id == model.id)

    conn.execute(insert)
    result = conn.execute(one)
    data = result.fetchone()

    m = ModelCaseNetwork.parse_obj(data)

    assert m == model


@pytest.mark.parametrize(
    "model", [ModelCaseDateTime() for n in range(NUM_TEST)]
)
def test_database_datetime(model: ModelCaseDateTime, conn):

    insert = ModelCaseDateTime.insert().values(model.dict())
    one = ModelCaseDateTime.select().where(ModelCaseDateTime.c.id == model.id)

    conn.execute(insert)
    result = conn.execute(one)
    data = result.fetchone()

    m = ModelCaseDateTime.parse_obj(data)

    assert m == model


@pytest.mark.parametrize("model", [ModelCaseEnum() for n in range(NUM_TEST)])
def test_database_enum(model: ModelCaseEnum, conn):

    insert = ModelCaseEnum.insert().values(model.dict())
    one = ModelCaseEnum.select().where(ModelCaseEnum.c.id == model.id)

    conn.execute(insert)
    result = conn.execute(one)
    data = result.fetchone()

    m = ModelCaseEnum.parse_obj(data)

    assert m == model


def test_database_update(conn):
    model = ModelUpdateDelete()
    insert = ModelUpdateDelete.insert().values(model.dict())

    update = (
        ModelUpdateDelete.update()
        .where(ModelUpdateDelete.c.id == model.id)
        .values(num=5)
    )
    one = ModelUpdateDelete.select().where(ModelUpdateDelete.c.id == model.id)

    conn.execute(insert)

    conn.execute(update)
    result_updated = conn.execute(one)
    data_updated = result_updated.fetchone()
    model_updated = ModelUpdateDelete.parse_obj(data_updated)

    assert model_updated.id == model.id
    assert model_updated.num != model.num
    assert model_updated.num == 5


def test_database_delete(conn):
    model = ModelUpdateDelete()
    insert = ModelUpdateDelete.insert().values(model.dict())
    c = model.c

    delete = ModelUpdateDelete.delete().where(c.id == model.id)
    query = ModelUpdateDelete.select()

    conn.execute(insert)
    results = conn.execute(query)
    data_before_delete = results.fetchall()
    conn.execute(delete)
    results = conn.execute(query)
    data_after_delete = results.fetchall()

    assert len(data_before_delete) == 1
    assert len(data_after_delete) == 0


class LeftTable(Base):
    a: str = "a"


class RightTable(Base):
    b: str = "b"
    left_id: UUID4 = Field(sa_args=[sa.ForeignKey(LeftTable.c.id)])


def test_database_join_with_pydantic_model(conn):

    left = LeftTable()
    insert_left = LeftTable.insert().values(left.dict())
    conn.execute(insert_left)

    right = RightTable(left_id=left.id)
    insert_right = RightTable.insert().values(right.dict())
    conn.execute(insert_right)

    join = RightTable.join(LeftTable, LeftTable.c.id == RightTable.c.left_id)
    query = sa.select([*RightTable.c, *LeftTable.c]).select_from(join)

    result_join = conn.execute(query)
    data = result_join.fetchall()

    assert data[0][0] == right.id
    assert data[0][2] == left.id


def test_database_join_with_table(conn):

    left = LeftTable()
    insert_left = LeftTable.insert().values(left.dict())
    conn.execute(insert_left)

    right = RightTable(left_id=left.id)
    insert_right = RightTable.insert().values(right.dict())
    conn.execute(insert_right)

    join = RightTable.join(
        LeftTable.__sa_table__, LeftTable.c.id == RightTable.c.left_id
    )
    query = sa.select([*RightTable.c, *LeftTable.c]).select_from(join)

    result_join = conn.execute(query)
    data = result_join.fetchall()

    assert data[0][0] == right.id
    assert data[0][2] == left.id
