import uuid

from validatable import UUID4, BaseTable, Field
from validatable import ForeignKey as fk
from validatable import MetaData, create_engine, validator

issubclass


class Base(BaseTable):
    metadata = MetaData()
    id: UUID4 = Field(default_factory=uuid.uuid4)


class User(Base):
    username: str = Field(max_length=16, sa_nullable=False, sa_unique=True)

    @validator("username")
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError("must be alphanumeric")
        return v


class Recipe(Base):
    title: str = Field(max_length=150, sa_nullable=False, sa_unique=True)
    owner: UUID4 = Field(sa_foreign_key=fk(User.c.id, ondelete="CASCADE"))


engine = create_engine("sqlite:///:memory:")
Base.__sa_metadata__.create_all(engine)


john = User(username="john")
feijoada = Recipe(title="Feijoada", owner=john.id)


with engine.connect() as conn:
    conn.execute(User.insert().values(john.dict()))
    conn.execute(Recipe.insert().values(feijoada.dict()))

    result = conn.execute(User.select())
    user = result.fetchone()
    print(User.parse_obj(user))

    result = conn.execute(Recipe.select())
    recipe = result.fetchone()
    print(Recipe.parse_obj(recipe))
