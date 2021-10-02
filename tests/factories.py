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

from validatable.main import BaseTable, MetaData

Faker.seed(0)
faker = Faker()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ UUID


class ModelUUID1(BaseTable, metadata=MetaData()):
    test: UUID1 = Field(default_factory=uuid.uuid1)


class ModelUUID3(BaseTable, metadata=MetaData()):
    test: UUID3 = Field(
        default_factory=lambda: uuid.uuid3(uuid.uuid4(), "name")
    )


class ModelUUID4(BaseTable, metadata=MetaData()):
    test: UUID4 = Field(default_factory=uuid.uuid4)


class ModelUUID5(BaseTable, metadata=MetaData()):
    test: UUID5 = Field(
        default_factory=lambda: uuid.uuid5(uuid.uuid4(), "name")
    )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Number


class ModelInt(BaseTable, metadata=MetaData()):

    test: int = Field(
        default_factory=lambda: random.randint(-2147483648, 2147483647)
    )


class ModelConInt(BaseTable, metadata=MetaData()):
    test: conint() = Field(  # type: ignore[valid-type]
        default_factory=lambda: random.randint(-2147483648, 2147483647)
    )


class ModelFloat(BaseTable, metadata=MetaData()):
    test: float = Field(
        default_factory=lambda: random.uniform(
            -3.402823466e38, 1.175494351e-38
        )
    )


class ModelConFloat(BaseTable, metadata=MetaData()):
    test: confloat() = Field(  # type: ignore[valid-type]
        default_factory=lambda: random.uniform(
            -3.402823466e38, 1.175494351e-38
        )
    )


class ModelDecimal(BaseTable, metadata=MetaData()):
    test: Decimal = Field(
        default_factory=lambda: Decimal(
            f"{random.uniform(-1000000000, 1000000000):.10f}"
        )
    )


class ModelConDecimal(BaseTable, metadata=MetaData()):
    test: condecimal() = Field(  # type: ignore[valid-type]
        default_factory=lambda: Decimal(
            f"{random.uniform(-1000000000, 1000000000):.10f}"
        )  # noqa E501
    )


class ModelPositiveInt(BaseTable, metadata=MetaData()):
    test: PositiveInt = Field(
        default_factory=lambda: random.randint(0, 2147483647)
    )


class ModelNegativeInt(BaseTable, metadata=MetaData()):
    test: NegativeInt = Field(
        default_factory=lambda: random.randint(-2147483648, 0)
    )


class ModelPositiveFloat(BaseTable, metadata=MetaData()):
    test: PositiveFloat = Field(
        default_factory=lambda: random.uniform(0, 1.175494351e-38)
    )


class ModelNegativeFloat(BaseTable, metadata=MetaData()):
    test: NegativeFloat = Field(
        default_factory=lambda: random.uniform(-3.402823466e38, 0)
    )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ String Bytes


class ModelStr(BaseTable, metadata=MetaData()):
    test: str = Field(default_factory=faker.sentence, sa_primary_key=True)


class ModelConStr(BaseTable, metadata=MetaData()):
    test: constr(max_length=10) = Field(  # type: ignore[valid-type]
        default_factory=lambda: f"{faker.sentence()}"[:10]
    )


class ModelEmailStr(BaseTable, metadata=MetaData()):
    test: EmailStr = Field(default_factory=faker.email)


class ModelNameEmail(BaseTable, metadata=MetaData()):
    # NameEmail do not allow points "." in validation. Example: 'Mr.', 'Jr.'
    # https://github.com/samuelcolvin/pydantic/issues/2955
    test: NameEmail = Field(
        default_factory=lambda: NameEmail(
            name=faker.name().replace(".", ""), email=faker.email()
        )
    )


class ModelPath(BaseTable, metadata=MetaData()):
    test: pathlib.Path = Field(
        default_factory=lambda: pathlib.PosixPath(
            faker.file_path(depth=random.randint(1, 5))
        )
    )


class ModelBytes(BaseTable, metadata=MetaData()):
    test: bytes = Field(default_factory=lambda: os.urandom(10))


class ModelConBytes(BaseTable, metadata=MetaData()):
    test: conbytes(max_length=10) = Field(  # type: ignore[valid-type]
        default_factory=lambda: os.urandom(10)
    )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Network


class ModelIPv4Address(BaseTable, metadata=MetaData()):
    test: IPv4Address = Field(default_factory=lambda: ip_address(faker.ipv4()))


class ModelIPv4Interface(BaseTable, metadata=MetaData()):
    test: IPv4Interface = Field(
        default_factory=lambda: ip_interface(faker.ipv4(network=True))
    )


class ModelIPv4Network(BaseTable, metadata=MetaData()):
    test: IPv4Network = Field(
        default_factory=lambda: ip_network(faker.ipv4(network=True))
    )


class ModelIPv6Address(BaseTable, metadata=MetaData()):
    test: IPv6Address = Field(default_factory=lambda: ip_address(faker.ipv6()))


class ModelIPv6Interface(BaseTable, metadata=MetaData()):
    test: IPv6Interface = Field(
        default_factory=lambda: ip_interface(faker.ipv6(network=True))
    )


class ModelIPv6Network(BaseTable, metadata=MetaData()):
    test: IPv6Network = Field(
        default_factory=lambda: ip_network(faker.ipv6(network=True))
    )


class ModelIPvAnyAddress(BaseTable, metadata=MetaData()):
    test: IPvAnyAddress = Field(
        default_factory=lambda: ip_address(
            faker.ipv6() if random.choice([True, False]) else faker.ipv4()
        )
    )


class ModelIPvAnyInterface(BaseTable, metadata=MetaData()):
    test: IPvAnyInterface = Field(
        default_factory=lambda: ip_interface(
            faker.ipv6(network=True)
            if random.choice([True, False])
            else faker.ipv4(network=True)
        )
    )


class ModelIPvAnyNetwork(BaseTable, metadata=MetaData()):
    test: IPvAnyNetwork = Field(
        default_factory=lambda: ip_network(
            faker.ipv6(network=True)
            if random.choice([True, False])
            else faker.ipv4(network=True)
        )
    )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ datetime


class ModelDatetime(BaseTable, metadata=MetaData()):
    test: dt.datetime = Field(default_factory=faker.date_time_between)


class ModelDate(BaseTable, metadata=MetaData()):
    test: dt.date = Field(default_factory=faker.date_between)


class ModelTime(BaseTable, metadata=MetaData()):
    test: dt.time = Field(default_factory=faker.time_object)


class ModelTimedelta(BaseTable, metadata=MetaData()):
    test: dt.timedelta = Field(
        default_factory=lambda: dt.timedelta(
            seconds=random.randint(0, 999999999)
        )
    )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Enum


class CaseEnum(enum.Enum):
    a: str = "a1"
    b: str = "b2"
    c: str = "c3"


class CaseIntEnum(enum.IntEnum):
    a: int = 1
    b: int = 2
    c: int = 3


class ModelEnum(BaseTable, metadata=MetaData()):
    test: CaseEnum = Field(
        default_factory=lambda: getattr(
            CaseEnum, random.choice(list(CaseEnum.__members__.keys()))
        )
    )


class ModelIntEnum(BaseTable, metadata=MetaData()):
    test: CaseIntEnum = Field(
        default_factory=lambda: getattr(
            CaseIntEnum, random.choice(list(CaseIntEnum.__members__.keys()))
        )
    )
