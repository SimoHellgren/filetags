from pathlib import Path
from sqlite3 import Connection

from filetags import crud
from filetags.models.node import Node


def attach_tree(
    conn: Connection, file_id: int, node: Node, parent_id: int | None = None
):
    tag_id = crud.tag.get_or_create(conn, node.value)
    filetag_id = crud.file_tag.attach(conn, file_id, tag_id, parent_id)
    for child in node.children:
        attach_tree(conn, file_id, child, filetag_id)


def add_tags_to_files(
    conn: Connection, files: list[Path], tags: list[Node], apply_tagalongs: bool = True
):
    file_ids = [x["id"] for x in crud.file.get_or_create_many(conn, files)]

    for file_id in file_ids:
        for tag in tags:
            attach_tree(conn, file_id, tag)

    if apply_tagalongs:
        crud.tagalong.apply(
            conn,
            file_ids,
        )
