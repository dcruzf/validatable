import sqlalchemy as sa
from pydantic import BaseModel
from pydantic.fields import ModelField
from pydantic.main import ModelMetaclass
from sqlalchemy.sql.schema import MetaData

from validatable.inference import get_column


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
        if isinstance(table, sa.Table):
            return super().__new__(mcls, name, bases, namespace, **kwargs)

        metadata = namespace.get("__sa_metadata__", None)
        if metadata is None:
            namespace["__sa_metadata__"] = namespace.pop("metadata", None)
            return super().__new__(mcls, name, bases, namespace, **kwargs)

        tablename = namespace.get("__sa_tablename__", name.lower())
        table_args = namespace.get("__sa_table_args__", [])
        table_kwargs = namespace.get("__sa_table_kwargs__", {})
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        columns = [
            get_column(v)
            for k, v in cls.__fields__.items()
            if hasattr(v, "__class__") and isinstance(v, ModelField)
        ]

        cls.__sa_table__ = sa.Table(
            tablename, metadata, *columns, *table_args, **table_kwargs
        )
        return cls

    @property
    def c(cls):
        return cls.__sa_table__.c

    @property
    def metadata(cls) -> MetaData:
        return cls.__sa_metadata__


class BaseTable(BaseModel, metaclass=ValidatableMetaclass):
    @property
    def c(self):
        """
        columns
        """
        return self.__sa_table__.c

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
