from pathlib import Path
from sqlite3 import Connection

import click

from filetags import crud


@click.group(help="Tagalong management")
@click.pass_obj
def tagalong(vault: Connection):
    pass


@tagalong.command(help="Register new tagalongs.")
@click.option("-t", "--tag", required=True, multiple=True)
@click.option("-ta", "--tagalong", required=True, multiple=True)
@click.pass_obj
def add(vault: Connection, tag: tuple[str, ...], tagalong: tuple[str, ...]):
    with vault as conn:
        for source in tag:
            source_id = crud.tag.get_or_create(conn, source)
            for target in tagalong:
                target_id = crud.tag.get_or_create(conn, target)

                crud.tagalong.add(conn, source_id, target_id)


@tagalong.command(help="Remove tagalongs.")
@click.option("-t", "--tag", required=True, multiple=True)
@click.option("-ta", "--tagalong", required=True, multiple=True)
@click.pass_obj
def remove(vault: Connection, tag: tuple[str, ...], tagalong: tuple[str, ...]):
    with vault as conn:
        for source in tag:
            source_record = crud.tag.get_by_name(conn, source)

            if not source_record:
                continue

            for target in tagalong:
                target_record = crud.tag.get_by_name(conn, target)

                if not target_record:
                    continue

                crud.tagalong.remove(conn, source_record[0], target_record[0])


@tagalong.command(help="Show all tagalongs.")
@click.pass_obj
def ls(vault: Connection):
    # TODO: Consider adding a grep-like filter if such would prove to be useful
    with vault as conn:
        for tag, tagalong in crud.tagalong.get_all_names(conn):
            click.echo(f"{tag} -> {tagalong}")


@tagalong.command(help="Apply all tagalongs (to all files by default).")
@click.option(
    "-f", "--file", type=click.Path(path_type=Path, exists=True), multiple=True
)
@click.pass_obj
def apply(vault: Connection, file: tuple[Path, ...]):
    # TODO: consider filtering by tag
    with vault as conn:
        file_ids = [crud.file.get_by_name(conn, str(path))[0] for path in file]

        crud.tagalong.apply(conn, file_ids)
