import sqlalchemy as sa
from pydantic.main import ModelMetaclass
from sqlalchemy.sql.schema import MetaData


class ValidatableMetaclass(ModelMetaclass):
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

        # __sa_tablename__ = namespace.get("__sa_tablename__")
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        return cls
