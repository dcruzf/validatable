import sqlalchemy as sa
from pydantic import BaseModel
from pydantic.fields import ModelField
from pydantic.main import ModelMetaclass
from sqlalchemy.sql.schema import MetaData

from validatable.util import get_column


class ValidatableMetaclass(ModelMetaclass):
    def table(cls) -> sa.Table:
        return cls.__sa_table__

    @classmethod
    def __prepare__(mcls, name, bases, *, metadata=None, **kwargs):

        if isinstance(metadata, MetaData):
            return {"__sa_metadata__": metadata}
        elif metadata is None:
            return {}
        else:
            raise TypeError("metadata must be a sqlalquemy metadata")

    def __new__(mcls, name, bases, namespace, metadata=None, **kwargs):

        table = namespace.get("__sa_table__")
        if isinstance(table, sa.Table):
            return super().__new__(mcls, name, bases, namespace, **kwargs)

        metadata = namespace.get("__sa_metadata__")
        if metadata is None:
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


class BaseTable(BaseModel, metaclass=ValidatableMetaclass):
    ...
