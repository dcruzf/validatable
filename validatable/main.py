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
from sqlalchemy.sql.schema import MetaData

from .inference import get_table


class ValidatableMetaclass(ModelMetaclass):
    """Extends ModelMetaclass to include SQLAlchemy Table logic."""

    @classmethod
    def __prepare__(mcls, name, bases, *, metadata=None, **kwargs):  # type: ignore[no-untyped-def] # noqa: E501
        """Set metadata before the evaluation of the class body."""
        if isinstance(metadata, MetaData):
            return {"__sa_metadata__": metadata, "__create_table__": True}

        elif metadata is None:

            if bases and hasattr(bases[0], "__sa_metadata__"):
                return {
                    "__sa_metadata__": bases[0].__sa_metadata__,
                    "__create_table__": bases[0].__create_table__,
                }
            else:
                return {}

        else:
            raise TypeError("metadata must be a sqlalquemy metadata")

    def __new__(mcls, name, bases, namespace, metadata=None, **kwargs):  # type: ignore[no-untyped-def] # noqa: E501
        """Control the BaseTable definition."""
        table = namespace.get("__sa_table__")
        if isinstance(table, Table):
            return super().__new__(mcls, name, bases, namespace, **kwargs)

        metadata = namespace.get("__sa_metadata__", None)
        if metadata is None:
            namespace["__sa_metadata__"] = namespace.pop("metadata", None)
            namespace["__create_table__"] = namespace.get(
                "__create_table__", True
            )
            return super().__new__(mcls, name, bases, namespace, **kwargs)

        tablename = namespace.get("__sa_tablename__", name.lower())
        namespace["__sa_tablename__"] = tablename

        table_args = namespace.get("__sa_table_args__", [])
        namespace["__sa_table_args__"] = table_args

        table_kwargs = namespace.get("__sa_table_kwargs__", {})
        namespace["__sa_table_kwargs__"] = table_kwargs

        exclude = namespace.get("__sa_exclude__")

        cls = super().__new__(mcls, name, bases, namespace, **kwargs)

        if cls.__create_table__:
            cls.__create_table__ = False
            cls.__sa_table__ = get_table(
                tablename,
                metadata,
                cls.__fields__,
                table_args,
                table_kwargs,
                exclude,
            )
        else:
            cls.__sa_table__ = None
            cls.__sa_metadata__ = None
            cls.__sa_table_args__ = []
            cls.__sa_table_kwargs__ = {}
            cls.__sa_exclude__ = None
        return cls

    @property
    def c(cls) -> ImmutableColumnCollection:  # type: ignore[type-arg]
        """Return the collection of columns."""
        return cls.__sa_table__.c  # type: ignore[attr-defined]

    @property
    def t(cls) -> Optional[Table]:
        """Return the table."""
        return cls.__sa_table__  # type: ignore[attr-defined]

    @property
    def metadata(cls) -> Optional[MetaData]:
        """Return the metadata instance."""
        return cls.__sa_metadata__  # type: ignore[attr-defined]


class BaseTable(BaseModel, metaclass=ValidatableMetaclass):
    """Extends BaseModel to include SQLAlchemy Table construction."""

    __sa_table__: Optional[Table]
    __sa_metadata__: Optional[MetaData]
    __sa_table_args__: List[Any]
    __sa_table_kwargs__: Dict[str, Any]
    __sa_exclude__: Optional[Set[str]] = None


class Validatable(BaseModel, metaclass=ValidatableMetaclass):
    """Extends BaseModel to include SQLAlchemy Table construction."""

    __sa_table__: Optional[Table]
    __sa_metadata__: Optional[MetaData]
    __sa_table_args__: List[Any]
    __sa_table_kwargs__: Dict[str, Any]
    __sa_exclude__: Optional[Set[str]] = None
