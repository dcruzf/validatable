import uuid

import sqlalchemy as sa


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
    Uses str(value) to bind parametre type.
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
