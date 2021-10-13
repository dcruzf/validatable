from typing import Type

import pytest
from conftest import NUM_REPETITIONS
from factories import (
    ModelAnyHttpUrl,
    ModelAnyUrl,
    ModelBool,
    ModelBytes,
    ModelConBytes,
    ModelConDecimal,
    ModelConFloat,
    ModelConInt,
    ModelConStr,
    ModelDate,
    ModelDatetime,
    ModelDecimal,
    ModelEmailStr,
    ModelEnum,
    ModelFloat,
    ModelHttpUrl,
    ModelInt,
    ModelIntEnum,
    ModelIPv4Address,
    ModelIPv4Interface,
    ModelIPv4Network,
    ModelIPv6Address,
    ModelIPv6Interface,
    ModelIPv6Network,
    ModelIPvAnyAddress,
    ModelIPvAnyInterface,
    ModelIPvAnyNetwork,
    ModelNameEmail,
    ModelNegativeFloat,
    ModelNegativeInt,
    ModelPath,
    ModelPositiveFloat,
    ModelPositiveInt,
    ModelStr,
    ModelStrictBool,
    ModelStrictUrl,
    ModelTime,
    ModelTimedelta,
    ModelUUID1,
    ModelUUID3,
    ModelUUID4,
    ModelUUID5,
)

from validatable import BaseTable


def make_params(*Models, repeat: int = NUM_REPETITIONS):
    param = []
    ids = []
    for Model in Models:
        param.extend([(Model, Model()) for n in range(repeat)])
        ids.extend([Model.__name__.replace("Model", "")] * repeat)
    return ids, param


ids, params = make_params(
    ModelInt,
    ModelUUID1,
    ModelUUID3,
    ModelUUID4,
    ModelUUID5,
    ModelConInt,
    ModelFloat,
    ModelConFloat,
    ModelDecimal,
    ModelConDecimal,
    ModelPositiveInt,
    ModelPositiveFloat,
    ModelNegativeFloat,
    ModelNegativeInt,
    ModelStr,
    ModelConStr,
    ModelBytes,
    ModelConBytes,
    ModelEmailStr,
    ModelNameEmail,
    ModelPath,
    ModelIPv4Address,
    ModelIPv4Interface,
    ModelIPv4Network,
    ModelIPv6Address,
    ModelIPv6Interface,
    ModelIPv6Network,
    ModelIPvAnyAddress,
    ModelIPvAnyInterface,
    ModelIPvAnyNetwork,
    ModelDate,
    ModelDatetime,
    ModelTime,
    ModelTimedelta,
    ModelEnum,
    ModelIntEnum,
    ModelHttpUrl,
    ModelAnyUrl,
    ModelAnyHttpUrl,
    ModelStrictUrl,
    ModelBool,
    ModelStrictBool,
)


@pytest.mark.parametrize(
    "Model, instance",
    params[::NUM_REPETITIONS],
    ids=[i.strip() for i in ids[::NUM_REPETITIONS]],
)
def test_factories(Model, instance):
    assert Model(**instance.dict()) == instance


@pytest.mark.filterwarnings(
    r"ignore:Dialect sqlite\+pysqlite does \*not\* "
    r"support Decimal objects natively"
)
@pytest.mark.parametrize("Model, instance", params, ids=ids)
def test_type_(Model: Type[BaseTable], instance: BaseTable, make_conn):
    create = Model.insert().values(instance.dict())
    read = Model.select().where(
        Model.c.test == instance.test  # type: ignore[attr-defined]
    )
    conn = make_conn(Model)
    conn.execute(create)
    result = conn.execute(read)
    data = result.fetchone()

    m = Model.construct(**data)
    assert m == instance
