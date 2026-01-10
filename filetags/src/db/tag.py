from sqlite3 import Connection
from typing import Optional


def create_tag(conn: Connection, name: str, category: Optional[str] = None):
    result = conn.execute(
        """INSERT INTO tag(name, category) VALUES (?, ?) RETURNING id,name,category""",
        (name, category),
    ).fetchone()

    return result


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

    update_stmt = ",\n".join(f"SET {col} = ?" for col in data)
    name_phs = ",".join("?" for _ in names)
    q = f"""
        UPDATE tag
            {update_stmt}
        WHERE name in ({name_phs})
    """

    vals = tuple([*data.values(), *names])
    conn.execute(q, vals)
