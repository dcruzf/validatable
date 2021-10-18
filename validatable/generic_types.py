import uuid

import sqlalchemy as sa
from typing import Any
from pydantic.json import pydantic_encoder
import json
from functools import partial


class SLBigInteger(sa.types.TypeDecorator):

    cache_ok = True
    impl = sa.BigInteger

    def load_dialect_impl(self, dialect):
        if dialect.name == "sqlite":
            return dialect.type_descriptor(sa.dialects.sqlite.INTEGER)
        else:
            return dialect.type_descriptor(sa.BigInteger)


class GUID(sa.types.TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses
    BINARY(16), to store UUID.
    """

    cache_ok = True
    impl = sa.types.BINARY

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(
                sa.dialects.postgresql.UUID(as_uuid=True)
            )
        else:
            return dialect.type_descriptor(sa.types.BINARY(16))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if dialect.name == "postgresql":
            return value
        else:
            return value.bytes

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return value
        else:
            return uuid.UUID(bytes=value)

    @property
    def python_type(self):
        return uuid.UUID


class AutoString(sa.types.TypeDecorator):
    """Platform-independent String type.
    Uses str(value) to bind parameter type.
    """

    cache_ok = True
    impl = sa.types.String
    length = 512
    serializer = str

    @staticmethod
    def deserializer(v):
        return v

    def __init__(
        self,
        length=None,
        collation=None,
        convert_unicode=False,
        unicode_error=None,
        _warn_on_bytestring=False,
        _expect_unicode=False,
        serializer=None,
        deserializer=None,
    ):
        self.serializer = serializer or self.serializer
        self.deserializer = deserializer or self.deserializer

        super().__init__(
            length=length,
            collation=collation,
            convert_unicode=convert_unicode,
            unicode_error=unicode_error,
            _warn_on_bytestring=_warn_on_bytestring,
            _expect_unicode=_expect_unicode,
        )

    def load_dialect_impl(self, dialect):
        if dialect.name in ("mysql", "mariadb"):
            return dialect.type_descriptor(sa.types.String(self.length))
        return dialect.type_descriptor(sa.types.String)

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, str):
            return value
        else:
            return self.serializer(value)

    def process_result_value(self, value, dialect):
        return self.deserializer(value)

    @property
    def python_type(self):
        return str


dumps = partial(json.dumps, default=pydantic_encoder)


class AutoJson(sa.types.TypeDecorator):
    """Json type with serialization"""

    cache_ok = True
    impl = sa.types.JSON

    @staticmethod
    def deserializer(v):
        return v

    def __init__(
        self,
        serializer=dumps,
        deserializer=lambda x: x,
        python_type=Any,
        none_as_null=False,
    ):
        self.serializer = serializer
        self.deserializer = deserializer
        self._python_type = python_type

        super().__init__(none_as_null=none_as_null)

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(self.impl)

    def process_bind_param(self, value, dialect):
        return self.serializer(value)

    def process_result_value(self, value, dialect):
        return self.deserializer(value)

    @property
    def python_type(self):
        return self._python_type
