import sqlite3

import pytest

from filetags.db.init import SCHEMA_PATH
from filetags.models.node import Node


@pytest.fixture
def conn():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA_PATH.read_text())
    yield conn
    conn.close()


@pytest.fixture
def nodes() -> list[Node]:
    n1 = Node(1)
    n2 = Node(2, parent=n1)
    n3 = Node(3, parent=n2)  # leaf
    n4 = Node(4, parent=n2)  # leaf
    n5 = Node(5, parent=n1)  # leaf
    n6 = Node(6, parent=n1)
    n7 = Node(7, parent=n6)
    n8 = Node(8, parent=n7)  # leaf

    return [n1, n2, n3, n4, n5, n6, n7, n8]
