from typing import Any, List, Optional

from pydantic.fields import FieldInfo, Undefined
from pydantic.typing import NoArgAnyCallable
from sqlalchemy import ForeignKey


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
    sa_primary_key: Optional[bool] = False,
    sa_pk: Optional[bool] = False,
    sa_nullable: Optional[bool] = None,
    sa_index: Optional[bool] = None,
    sa_unique: Optional[bool] = None,
    sa_args: List[Any] = None,
    sa_foreign_key: Optional[ForeignKey] = None,
    sa_fk: Optional[ForeignKey] = None,
    **extra: Any,
) -> Any:
    extra["sa_primary_key"] = sa_primary_key
    extra["sa_pk"] = sa_pk
    extra["sa_nullable"] = sa_nullable
    extra["sa_index"] = sa_index
    extra["sa_unique"] = sa_unique
    extra["sa_args"] = sa_args or []
    extra["sa_foreign_key"] = sa_foreign_key
    extra["sa_fk"] = sa_fk

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
