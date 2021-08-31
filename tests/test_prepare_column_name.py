import pytest
import sqlalchemy as sa

from validatable.util import prepare_column_name


@pytest.mark.parametrize(
    ("column", "column_name"),
    [
        (sa.Column("samename", sa.String), "samename"),
        (sa.Column(sa.String), "None"),
    ],
    ids=["same name", "None"],
)
def test_correct_column_name(column: sa.Column, column_name: str):

    result = prepare_column_name(column, column_name)
    assert result.name == column_name


@pytest.mark.parametrize(
    ("column", "column_name"),
    [
        (sa.Column("different", sa.String), "name"),
    ],
    ids=["different name"],
)
def test_incorrect_column_name(column: sa.Column, column_name: str):

    with pytest.raises(ValueError):
        prepare_column_name(column, column_name)
