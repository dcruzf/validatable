"""
The main module provides the definition of Validatable BaseTable.

It defines ValidatableMetaclass, which is a customization of BaseTable
creation that includes the instantiation of a SQLAlchemy Table object.

BaseTable class extends Pydantic BaseModel to include SQLAlchemy Table
instance methods in the class interface.

"""
from typing import Any, Dict, List, Optional, Set

from pydantic import BaseModel
from pydantic.main import ModelMetaclass
from sqlalchemy import Table
from sqlalchemy.sql.base import ImmutableColumnCollection
from sqlalchemy.sql.dml import Delete, Insert, Update
from sqlalchemy.sql.schema import MetaData
from sqlalchemy.sql.selectable import Join, Select

from .inference import get_table


class ValidatableMetaclass(ModelMetaclass):
    """Extends ModelMetaclass to include SQLAlchemy Table logic."""

    @classmethod
    def __prepare__(mcls, name, bases, *, metadata=None, **kwargs):
        """Set metadata before the evaluation of the class body."""
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
        """Control the BaseTable definition."""
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
        """Return the collection of columns."""
        return cls.__sa_table__.c  # type: ignore[attr-defined]

    @property
    def metadata(cls) -> MetaData:
        """Return the metadata instance."""
        return cls.__sa_metadata__  # type: ignore[attr-defined]


class BaseTable(BaseModel, metaclass=ValidatableMetaclass):
    """Extends BaseModel to include SQLAlchemy Table methods."""

    __sa_table__: Table
    __sa_metadata__: MetaData
    __sa_table_args__: List[Any]
    __sa_table_kwargs__: Dict[str, Any]
    __sa_exclude__: Optional[Set[str]] = None

    @property
    def c(cls) -> ImmutableColumnCollection:
        """Return the collection of columns."""
        return cls.__sa_table__.c

    @classmethod
    def insert(cls, values=None, inline=False, **kwargs) -> Insert:
        """
        Generate an Insert object for current BaseTable.

        E.g.::

            stmt = User.insert().values(name='John')
        """
        return cls.__sa_table__.insert(values=values, inline=inline, **kwargs)

    @classmethod
    def update(
        cls, whereclause=None, values=None, inline=False, **kwargs
    ) -> Update:
        """
        Generate an Update object for current BaseTable.

        E.g.::

            stmt = User.update().where(User.c.id==1).values(name='John Doe')
        """
        return cls.__sa_table__.update(
            whereclause=whereclause, values=values, inline=inline, **kwargs
        )

    @classmethod
    def delete(cls, whereclause=None, **kwargs) -> Delete:
        """
        Generate a Delete object for current BaseTable.

        E.g.::

            stmt = User.delete().where(User.c.id==1)
        """
        return cls.__sa_table__.delete(whereclause=whereclause, **kwargs)

    @classmethod
    def select(cls, whereclause=None, **kwargs) -> Select:
        """
        Generate a Select object for current BaseTable.

        E.g.::

            stmt = User.select().where(User.c.id == 1)
        """
        return cls.__sa_table__.select(whereclause=whereclause, **kwargs)

    @classmethod
    def join(cls, right, onclause=None, isouter=False, full=False) -> Join:
        """
        Return a `Join` between two tables.

        E.g.::

            j = User.join(Address,
                          User.c.id == Address.c.user_id)
            stmt = select(user_table).select_from(j)
        """
        if hasattr(right, "__sa_table__"):
            right = right.__sa_table__

        return cls.__sa_table__.join(
            right, onclause=onclause, isouter=isouter, full=full
        )
