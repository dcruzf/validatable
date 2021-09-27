<p align="center">
<img  width="150" height="150" src="https://raw.githubusercontent.com/dcruzf/validatable/main/docs/img/logo.svg">
</p>

<h1 align="center">Validatable</h1>

[![pre-commit](https://github.com/dcruzf/validatable/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/dcruzf/validatable/actions/workflows/pre-commit.yml)
[![test on Linux](https://github.com/dcruzf/validatable/actions/workflows/test_linux.yml/badge.svg)](https://github.com/dcruzf/validatable/actions/workflows/test_linux.yml)
[![test on MacOS](https://github.com/dcruzf/validatable/actions/workflows/test_mac.yml/badge.svg)](https://github.com/dcruzf/validatable/actions/workflows/test_mac.yml)

## Introduction

Validatable provides a single class definition for data validation and persistence in relational databases. It uses Pydantic and SQLAlchemy Core.

## Getting Started

### Installation

You can install Validatable like this:

```
pip install validatable
```

### Simple Example

```py
from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import ForeignKey, MetaData
from sqlalchemy.schema import CreateTable

from validatable import UUID4, BaseTable, EmailStr, Field


class Base(BaseTable):
    metadata = MetaData()


class User(Base):
    id: UUID4 = Field(sa_primary_key=True, default_factory=uuid4)
    name: str
    email: EmailStr
    created_ts: datetime = Field(default_factory=datetime.now)
    friends: Optional[int] = Field(None, sa_fk=ForeignKey("user.id"))


ddl = CreateTable(User.__sa_table__)
print(ddl)

# CREATE TABLE "user" (
#         id BINARY(16) NOT NULL,
#         name VARCHAR,
#         email VARCHAR(320),
#         created_ts DATETIME NOT NULL,
#         friends INTEGER NOT NULL,
#         PRIMARY KEY (id),
#         FOREIGN KEY(friends) REFERENCES "user" (id)
# )
```

## License

This project is licensed under the terms of the MIT license - see the LICENSE.txt file for details.
