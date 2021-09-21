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
        if isinstance(value, str):
            value = uuid.UUID(value)
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
            return str(value)

    def process_result_value(self, value, dialect):
        return value

    @property
    def python_type(self):
        return str
