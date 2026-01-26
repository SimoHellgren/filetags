from pathlib import Path
from typing import Sequence

import click

from filetags import crud, service
from filetags.commands.context import LazyVault


@click.group(help="File managament")
@click.pass_obj
def file(vault: LazyVault):
    pass


def print_box(title: str, lines: list[str]):
    width = max(len(click.unstyle(line)) for line in [title, *lines]) + 2

    click.echo(f"┌{'─' * width}┐")
    click.echo(f"│ {title.ljust(width - 1)}│")
    click.echo(f"├{'─' * width}┤")
    for line in lines:
        padding = width - 1 - len(click.unstyle(line))
        click.echo(f"│ {line}{' ' * padding}│")
    click.echo(f"└{'─' * width}┘")


def check_path(p: Path) -> dict:
    if p.exists():
        return {"text": "Exists", "fg": "green"}

    return {"text": "Not found", "fg": "red"}


def check_inode(p: Path, record: dict) -> dict:
    if not record["inode"]:
        return {"text": "Inode missing", "fg": "yellow"}

    if p.exists():
        stat = p.stat()

        if not (record["inode"] == stat.st_ino and record["device"] == stat.st_dev):
            return {"text": "Mismatch", "fg": "red"}

    return {"text": "OK", "fg": "green"}


@file.command(help="Show file info")
@click.argument("files", nargs=-1, type=click.Path(path_type=Path))
@click.pass_obj
def info(vault: LazyVault, files: tuple[Path, ...]):
    with vault as conn:
        files_with_tags = service.get_files_with_tags(conn, files)

    for path, data in files_with_tags.items():
        record = data["file"]
        roots = data["roots"]

        print_box(
            str(path),
            [
                f"Tags: {','.join(str(root) for root in roots)}",
                "Path: " + click.style(**check_path(path)),
                "Inode/device: " + click.style(**check_inode(path, record)),
            ],
        )


@file.command(help="Add files to db (without tags).")
@click.argument(
    "files", nargs=-1, type=click.Path(path_type=Path, exists=True, dir_okay=False)
)
@click.pass_obj
def add(vault: LazyVault, files: Sequence[Path]):
    with vault as conn:
        crud.file.get_or_create_many(conn, files)


@file.command(help="Drop files from db.")
@click.argument(
    "files", nargs=-1, type=click.Path(path_type=Path, exists=True, dir_okay=False)
)
@click.pass_obj
def drop(vault: LazyVault, files: Sequence[Path]):
    with vault as conn:
        records = crud.file.get_many_by_path(conn, files)
        click.confirm(
            f"Going do delete {len(records)} file(s). You sure about this", abort=True
        )
        for file in records:
            crud.file.delete(conn, file["id"])
