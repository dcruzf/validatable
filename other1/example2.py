from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy.dialects.postgresql import dialect
from sqlalchemy.schema import CreateTable

from validatable import UUID4, BaseTable, EmailStr, Field, ForeignKey, MetaData


class Base(BaseTable):
    metadata = MetaData()


class User(Base):
    id: UUID4 = Field(sa_primary_key=True, default_factory=uuid4)
    name: str
    email: EmailStr
    created_ts: datetime = Field(default_factory=datetime.now)
    friends: Optional[UUID4] = Field(sa_fk=ForeignKey("user.id"))


ddl = CreateTable(User.__sa_table__).compile(dialect=dialect())
print(ddl)
