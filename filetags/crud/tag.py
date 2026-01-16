from sqlite3 import Connection, Row
from typing import Optional


def create(conn: Connection, name: str, category: Optional[str] = None):
    result = conn.execute(
        """INSERT INTO tag(name, category) VALUES (?, ?) RETURNING id,name,category""",
        (name, category),
    ).fetchone()

    return result


def get_by_name(conn: Connection, name: str):
    result = conn.execute(
        "SELECT id, name, category FROM tag WHERE name = ?", (name,)
    ).fetchone()
    return result


def get_many_by_name(conn: Connection, names: list[str]) -> list[Row]:
    phs = ",".join("?" for _ in names)
    q = f"SELECT * FROM tag WHERE name IN ({phs})"
    return conn.execute(q, names).fetchall()


def get_all(conn: Connection):
    return conn.execute("SELECT * FROM tag").fetchall()


def get_or_create(conn: Connection, tag: str) -> int:
    q = """
        INSERT INTO tag(name) VALUES (?)
        ON CONFLICT (name) DO UPDATE SET name=name --no-op
        RETURNING id
    """
    (tag_id,) = conn.execute(q, (tag,)).fetchone()

    return tag_id


def get_or_create_many(conn: Connection, tags: list[str]) -> list[Row]:
    vals = ",".join("(?)" for _ in tags)

    q = f"""
        INSERT INTO tag(name) VALUES {vals}
        ON CONFLICT (name) DO UPDATE SET name=name --no-op
        RETURNING id
    """

    return conn.execute(q, tags).fetchall()


def update(conn: Connection, names: list[str], data: dict):
    ALLOWED_COLS = {"name", "category"}

    if forbidden := (data.keys() - ALLOWED_COLS):
        raise ValueError(f"Forbidden column(s): {forbidden}")

    update_stmt = ",\n".join(f"{col} = ?" for col in data)
    name_phs = ",".join("?" for _ in names)
    q = f"""
        UPDATE tag SET
            {update_stmt}
        WHERE name in ({name_phs})
    """

    vals = tuple([*data.values(), *names])
    conn.execute(q, vals)


def delete(conn: Connection, tag_id: int):
    conn.execute("DELETE FROM tag WHERE id = ?", (tag_id,))
