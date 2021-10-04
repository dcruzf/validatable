<p align="center">
<img  width="150" height="150" src="https://raw.githubusercontent.com/dcruzf/validatable/main/docs/img/logo.svg">
</p>

<h1 align="center">Validatable</h1>

_Data validation and SQL Toolkit using Python type hints._

[![CI](https://github.com/dcruzf/validatable/actions/workflows/tests.yml/badge.svg)](https://github.com/dcruzf/validatable/actions/workflows/tests.yml)
[![pre-commit](https://github.com/dcruzf/validatable/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/dcruzf/validatable/actions/workflows/pre-commit.yml)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/validatable)](https://pypi.org/project/validatable/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/dcruzf/validatable.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/dcruzf/validatable/context:python)
[![PyPI - License](https://img.shields.io/pypi/l/validatable)](https://raw.githubusercontent.com/dcruzf/validatable/main/LICENSE)
[![coverage.py report](https://img.shields.io/badge/dynamic/json?color=success&labelColor=success&label=coverage&logo=github&query=%24.totals.percent_covered_display&suffix=%25&url=https%3A%2F%2Fdcruzf.github.io%2Fvalidatable%2Fcov%2Fcoverage.json)](https://dcruzf.github.io/validatable/cov/)

## Introduction

Validatable provides a single class definition for data validation and SQL table representation. It uses Pydantic and SQLAlchemy Core.

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

# CREATE TABLE "user" (
#         id UUID NOT NULL,
#         name VARCHAR NOT NULL,
#         email VARCHAR(320) NOT NULL,
#         created_ts TIMESTAMP WITHOUT TIME ZONE,
#         friends UUID,
#         PRIMARY KEY (id),
#         FOREIGN KEY(friends) REFERENCES "user" (id)
# )
```

## License

This project is licensed under the terms of the MIT license - see the LICENSE.txt file for details.
