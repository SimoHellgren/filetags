from sqlite3 import Connection
from typing import Optional


def create_tag(conn: Connection, name: str, category: Optional[str] = None):
    result = conn.execute(
        """INSERT INTO tag(name, category) VALUES (?, ?) RETURNING id,name,category""",
        (name, category),
    ).fetchone()

    return result


def get_tag_by_name(conn: Connection, name: str):
    result = conn.execute(
        "SELECT id, name, category FROM tag WHERE name = ?", (name,)
    ).fetchone()
    return result


def get_all_tags(conn: Connection):
    return conn.execute("SELECT * FROM tag").fetchall()


def get_or_create_tag(conn: Connection, tag: str) -> int:
    q = """
        INSERT INTO tag(name) VALUES (?)
        ON CONFLICT (name) DO UPDATE SET name=name --no-op
        RETURNING id
    """
    (tag_id,) = conn.execute(q, (tag,)).fetchone()

    return tag_id


def update_tags(conn: Connection, names: list[str], data: dict):
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


def delete_tag(conn: Connection, tag_id: int):
    conn.execute("DELETE FROM tag WHERE id = ?", (tag_id,))
