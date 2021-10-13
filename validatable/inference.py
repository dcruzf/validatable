from typing import Any, Dict, List, Optional, Set, Tuple, Union

import sqlalchemy as sa
from pydantic.fields import ModelField, UndefinedType

from .type_dispatch import get_sql_type


def prepare_column_name(column: sa.Column, column_name: str) -> sa.Column:
    if column.name == column_name:
        return column

    if column.name is None:
        column.name = column_name
        return column

    raise ValueError(
        "Column name must be equal to field name, or field alias, or None"
    )


def primary_key_kwargs(col_kwargs: Dict[str, Any]):
    pk = col_kwargs.pop("pk", False)
    return col_kwargs.get("primary_key") or pk


def nullable_kwargs(
    col_kwargs: Dict[str, Any], required: Union[bool, UndefinedType], pk: bool
):
    nullable = col_kwargs.get("nullable")
    if pk:
        return nullable
    return nullable if nullable is not None else not required


def get_sa_args_kwargs(m: ModelField) -> Tuple[Any, Dict[str, Any]]:
    keys = tuple(m.field_info.extra.keys())
    col_kwargs = {
        k[3:]: m.field_info.extra.pop(k) for k in keys if k.startswith("sa_")
    }
    col_kwargs["primary_key"] = primary_key_kwargs(col_kwargs)
    col_kwargs["nullable"] = nullable_kwargs(
        col_kwargs, m.required, col_kwargs["primary_key"]
    )

    args = col_kwargs.pop("args", [])
    fk = col_kwargs.pop("fk", None)
    fk = col_kwargs.pop("foreign_key", None) or fk
    args.append(fk)
    return args, col_kwargs


def get_column(m: ModelField) -> sa.Column:
    args, col_kwargs = get_sa_args_kwargs(m)
    column = col_kwargs.pop("column", None)

    if isinstance(column, sa.Column):
        return prepare_column_name(column, m.alias)

    column_type = col_kwargs.pop("type", None) or col_kwargs.pop("type_", None)

    if column_type:
        return sa.Column(m.alias, column_type, *args, **col_kwargs)

    sa_type = get_sql_type(m)
    return sa.Column(m.alias, sa_type, *args, **col_kwargs)


def is_model_field(v: Any) -> bool:
    return hasattr(v, "__class__") and isinstance(v, ModelField)


def get_table(
    name: str,
    metadata: sa.MetaData,
    fields: Dict[str, Any],
    table_args: List[str],
    table_kwargs: Dict[str, Any],
    exclude: Optional[Set[str]] = None,
) -> sa.Table:

    exclude = exclude or set()
    columns = [
        get_column(v)
        for k, v in fields.items()
        if k not in exclude and is_model_field(v)
    ]
    return sa.Table(name, metadata, *columns, *table_args, **table_kwargs)
