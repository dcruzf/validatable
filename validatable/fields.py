from typing import Any, List, Optional

import sqlalchemy as sa
from pydantic.fields import FieldInfo, Undefined
from pydantic.typing import NoArgAnyCallable

sa.Column


def Field(
    default: Any = Undefined,
    *,
    default_factory: Optional[NoArgAnyCallable] = None,
    alias: str = None,
    title: str = None,
    description: str = None,
    const: bool = None,
    gt: float = None,
    ge: float = None,
    lt: float = None,
    le: float = None,
    multiple_of: float = None,
    min_items: int = None,
    max_items: int = None,
    min_length: int = None,
    max_length: int = None,
    allow_mutation: bool = True,
    regex: str = None,
    primary_key: Optional[bool] = False,
    foreign_key: Optional[sa.ForeignKey] = None,
    nullable: Optional[bool] = None,
    index: Optional[bool] = None,
    unique: Optional[bool] = None,
    sa_args: List[Any] = None,
    **extra: Any,
) -> Any:
    extra["sa_primary_key"] = primary_key
    extra["sa_foreign_key"] = foreign_key
    extra["sa_nullable"] = nullable
    extra["sa_index"] = index
    extra["sa_unique"] = unique

    field_info = FieldInfo(
        default,
        default_factory=default_factory,
        alias=alias,
        title=title,
        description=description,
        const=const,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        multiple_of=multiple_of,
        min_items=min_items,
        max_items=max_items,
        min_length=min_length,
        max_length=max_length,
        allow_mutation=allow_mutation,
        regex=regex,
        **extra,
    )
    field_info._validate()
    return field_info
