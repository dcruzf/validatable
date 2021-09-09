import pytest

from validatable.fields import Field
from sqlalchemy import ForeignKey


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


def test_sa_foreign_key():
    fk = ForeignKey("table.id")

    field = Field(sa_foreign_key=fk)

    assert field.extra["sa_args"] == [fk]
