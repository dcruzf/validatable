import pytest
import sqlalchemy as sa

from validatable.util import prepare_column_name


def test_same_column_name(column: sa.Column, column_name: str):

    result = prepare_column_name(
        sa.Column("column_name", sa.String), "column_name"
    )
    assert result.name == column_name


def test_none_column_name(column: sa.Column, column_name: str):

    result = prepare_column_name(sa.Column(sa.String), "column_name")
    assert result.name == column_name


def test_incorrect_column_name(column: sa.Column, column_name: str):

    with pytest.raises(ValueError):
        prepare_column_name(sa.Column("different", sa.String), "name")
