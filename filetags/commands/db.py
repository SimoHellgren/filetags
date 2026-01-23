from pathlib import Path
from sqlite3 import Connection

import click

from filetags.db.init import init_db


@click.group(help="Database management")
@click.pass_obj
def db(vault: Connection):
    pass


@db.command(help="Initialize empty vault")
@click.argument("filepath", type=click.Path(path_type=Path), default="vault.db")
def init(filepath: Path):
    if filepath.exists():
        click.echo(f"{filepath} already exists.")

    else:
        init_db(filepath)
        click.echo(f"{filepath} created.")
