import pytest
import sqlalchemy as sa
from sqlalchemy import ForeignKey

from validatable.fields import Field
from validatable.main import BaseTable


@pytest.mark.parametrize(
    "kwarg",
    [
        {"sa_primary_key": True},
        {"sa_nullable": False},
        {"sa_index": True},
        {"sa_unique": True},
        {"sa_args": []},
    ],
)
def test_sa_arguments(kwarg):
    field = Field(**kwarg)
    key = tuple(kwarg.keys())[0]
    value = tuple(kwarg.values())[0]
    assert field.extra[key] == value


def test_model_primary_key():

    metadata = sa.MetaData()

    class Item(BaseTable, metadata=metadata):
        id: int = Field(sa_primary_key=True)
        name: str = Field("")

    assert Item.c.id.primary_key


def test_model_nullable():

    metadata = sa.MetaData()

    class Item(BaseTable, metadata=metadata):
        id: int = Field(sa_primary_key=True)
        name: str = Field("", sa_nullable=False)

    assert not Item.c.name.nullable


def test_model_index():

    metadata = sa.MetaData()

    class Item(BaseTable, metadata=metadata):
        id: int = Field(sa_primary_key=True)
        name: str = Field("", sa_index=True)

    assert Item.c.name.index


def test_model_unique():

    metadata = sa.MetaData()

    class Item(BaseTable, metadata=metadata):
        id: int = Field(sa_primary_key=True)
        name: str = Field("", sa_unique=True)

    assert Item.c.name.unique


def test_model_foreign_key():

    metadata = sa.MetaData()

    fk = ForeignKey("test.id")

    class Item(BaseTable, metadata=metadata):
        id: int = Field(sa_primary_key=True)
        name: str = Field("", sa_foreign_key=fk)

    assert len(Item.c.name.foreign_keys) == 1
    assert fk in Item.c.name.foreign_keys


def test_model_foreign_key_with_fk():

    metadata = sa.MetaData()

    class Item(BaseTable, metadata=metadata):
        id: int = Field(sa_primary_key=True)
        name: str = Field(
            "", sa_fk=sa.ForeignKey("test.id", ondelete="CASCADE")
        )

    fk = tuple(Item.c.name.foreign_keys)[0]

    assert len(Item.c.name.foreign_keys) == 1
    assert fk.target_fullname == "test.id"
