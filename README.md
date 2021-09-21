<p align="center">
<img  width="150" height="150" src="./docs/img/V.svg">
</p>

<h1 align="center">Validatable</h1>

[![Test MacOS](https://github.com/dcruzf/validatable/actions/workflows/test_mac.yml/badge.svg)](https://github.com/dcruzf/validatable/actions/workflows/test_mac.yml)
[![Test on Linux](https://github.com/dcruzf/validatable/actions/workflows/test_linux.yml/badge.svg)](https://github.com/dcruzf/validatable/actions/workflows/test_linux.yml)
[![Test MacOS](https://github.com/dcruzf/validatable/actions/workflows/test_mac.yml/badge.svg)](https://github.com/dcruzf/validatable/actions/workflows/test_mac.yml)

## Introduction

Validatable provides a single class definition for data validation and persistence in relational databases. It uses Pydantic and SQLAlchemy Core.

## Getting Started

### Installation

You can install Validatable like this:

```sh
pip install validatable
```

### Simple Example

```py
import uuid

from validatable import UUID4, BaseTable, Field
from validatable import ForeignKey as fk
from validatable import MetaData, create_engine, validator


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
    # id=UUID('193006cb-f10b-47e6-8bee-9fbabc5727ca')
    # username='john'

    result = conn.execute(Recipe.select())
    recipe = result.fetchone()
    print(Recipe.parse_obj(recipe))
    # id=UUID('f96e3a7c-67be-4b0a-bd33-134aef73585f')
    # title='Feijoada'
    # owner=UUID('193006cb-f10b-47e6-8bee-9fbabc5727ca')


```

## License

This project is licensed under the MIT License - see the LICENSE.txt file for details.
