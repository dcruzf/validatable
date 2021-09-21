from typing import Any, Dict, List, Optional, Set

from pydantic import BaseModel
from pydantic.main import ModelMetaclass
from sqlalchemy import Table
from sqlalchemy.sql.base import ImmutableColumnCollection
from sqlalchemy.sql.schema import MetaData

from .inference import get_table


class ValidatableMetaclass(ModelMetaclass):
    @classmethod
    def __prepare__(mcls, name, bases, *, metadata=None, **kwargs):

        if isinstance(metadata, MetaData):
            return {"__sa_metadata__": metadata}

        elif metadata is None:

            if bases and hasattr(bases[0], "__sa_metadata__"):
                return {"__sa_metadata__": bases[0].__sa_metadata__}
            else:
                return {}

        else:
            raise TypeError("metadata must be a sqlalquemy metadata")

    def __new__(mcls, name, bases, namespace, metadata=None, **kwargs):

        table = namespace.get("__sa_table__")
        if isinstance(table, Table):
            return super().__new__(mcls, name, bases, namespace, **kwargs)

        metadata = namespace.get("__sa_metadata__", None)
        if metadata is None:
            namespace["__sa_metadata__"] = namespace.pop("metadata", None)
            return super().__new__(mcls, name, bases, namespace, **kwargs)

        tablename = namespace.get("__sa_tablename__", name.lower())
        namespace["__sa_tablename__"] = tablename

        table_args = namespace.get("__sa_table_args__", [])
        namespace["__sa_table_args__"] = table_args

        table_kwargs = namespace.get("__sa_table_kwargs__", {})
        namespace["__sa_table_kwargs__"] = table_kwargs

        exclude = namespace.get("__sa_exclude__")

        cls = super().__new__(mcls, name, bases, namespace, **kwargs)

        cls.__sa_table__ = get_table(
            tablename,
            metadata,
            cls.__fields__,
            table_args,
            table_kwargs,
            exclude,
        )
        return cls

    @property
    def c(cls) -> ImmutableColumnCollection:
        return cls.__sa_table__.c  # type: ignore[attr-defined]

    @property
    def metadata(cls) -> MetaData:
        return cls.__sa_metadata__  # type: ignore[attr-defined]


class BaseTable(BaseModel, metaclass=ValidatableMetaclass):
    __sa_table__: Table
    __sa_metadata__: MetaData
    __sa_table_args__: List[Any]
    __sa_table_kwargs__: Dict[str, Any]
    __sa_exclude__: Optional[Set[str]] = None

    @property
    def c(cls) -> ImmutableColumnCollection:
        return cls.__sa_table__.c

    @classmethod
    def insert(cls, values=None, inline=False, **kwargs):
        """
        table.insert()

        """
        return cls.__sa_table__.insert(values=values, inline=inline, **kwargs)

    @classmethod
    def update(cls, whereclause=None, values=None, inline=False, **kwargs):
        """
        table.update()

        """
        return cls.__sa_table__.update(
            whereclause=whereclause, values=values, inline=inline, **kwargs
        )

    @classmethod
    def delete(cls, whereclause=None, **kwargs):
        """
        table.delete()

        """
        return cls.__sa_table__.delete(whereclause=whereclause, **kwargs)

    @classmethod
    def select(cls, whereclause=None, **kwargs):
        """
        table.select()

        """
        return cls.__sa_table__.select(whereclause=whereclause, **kwargs)

    @classmethod
    def join(cls, right, onclause=None, isouter=False, full=False):
        """
        table.join()

        """
        if hasattr(right, "__sa_table__"):
            right = right.__sa_table__

        return cls.__sa_table__.join(
            right, onclause=onclause, isouter=isouter, full=full
        )
