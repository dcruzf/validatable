from typing import List, Set, Tuple, Deque
from collections import deque
from validatable import BaseTable, MetaData


def test_list_type():
    class ListCase(BaseTable, metadata=MetaData()):
        name: list = [1, 2, 3]


def test_typing_list_type():
    class ListCase(BaseTable, metadata=MetaData()):
        name: List


def test_typing_list_type_with_subscription():
    class ListCase(BaseTable, metadata=MetaData()):
        name: List[int]


def test_set_type():
    class SetCase(BaseTable, metadata=MetaData()):
        name: set = [1, 2, 3]


def test_typing_set_type():
    class SetCase(BaseTable, metadata=MetaData()):
        name: Set


def test_typing_set_type_with_subscription():
    class SetCase(BaseTable, metadata=MetaData()):
        name: Set[int]


def test_tuple_type():
    class TupleCase(BaseTable, metadata=MetaData()):
        name: tuple = [1, 2, 3]


def test_typing_tuple_type():
    class TupleCase(BaseTable, metadata=MetaData()):
        name: Tuple


def test_typing_tuple_type_with_subscription():
    class TupleCase(BaseTable, metadata=MetaData()):
        name: Tuple[int]


def test_deque_type():
    class DequeCase(BaseTable, metadata=MetaData()):
        name: deque


def test_typing_deque_type():
    class DequeCase(BaseTable, metadata=MetaData()):
        name: Deque


def test_typing_deque_with_subscription():
    class DequeCase(BaseTable, metadata=MetaData()):
        name: Deque[int]


def test_type_tuple(make_conn):
    class Model(BaseTable, metadata=MetaData()):
        ft: Tuple = ("a", "b", 1, 1.2)
        f: tuple = ("a", "b", 1, 1.2)
        f_sub: Tuple[int, ...] = (1, 2, 3, 4)

    instance = Model()
    create = Model.insert().values(instance.dict())
    read = Model.select()
    conn = make_conn(Model)
    conn.execute(create)
    result = conn.execute(read)
    data = result.fetchone()
    m = Model.construct(data)
    assert m == instance


def test_type_set(make_conn):
    class Model(BaseTable, metadata=MetaData()):
        ft: Set = {"a", "b", 1, 1.2}
        f: set = {"a", "b", 1, 1.2}
        f_sub: Set[int] = {1, 2, 3, 4}

    instance = Model()
    create = Model.insert().values(instance.dict())
    read = Model.select()
    conn = make_conn(Model)
    conn.execute(create)
    result = conn.execute(read)
    data = result.fetchone()
    m = Model.construct(data)
    assert m == instance


def test_type_list(make_conn):
    class Model(BaseTable, metadata=MetaData()):
        ft: List = ["a", "b", 1, 1.2]
        f: list = ["a", "b", 1, 1.2]
        f_sub: List[int] = [1, 2, 3, 4]

    instance = Model()
    create = Model.insert().values(instance.dict())
    read = Model.select()
    conn = make_conn(Model)
    conn.execute(create)
    result = conn.execute(read)
    data = result.fetchone()
    m = Model.construct(data)
    assert m == instance
