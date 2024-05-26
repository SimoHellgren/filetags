from collections import defaultdict
import json
import click

# a vault is a mapping of filenames to tags
Vault = defaultdict[str, set[str]]


def load_vault(filename):
    with open(filename, "r") as f:
        converted_sets = {k: set(v) for k, v in json.load(f).items()}
        return defaultdict(set, converted_sets)


def save_vault(filename, data):
    with open(filename, "w") as f:
        # default handles conversion of sets to lists.
        # possibly need to do something more elegant later.
        json.dump(data, f, indent=2, default=list)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("vaultname")
def init_vault(vaultname):
    with open(vaultname, "w") as f:
        json.dump({}, f, indent=2)


def parse_tags(tags):
    return {tag.strip() for tag in tags.split(",")}


@cli.command()
@click.argument("vault", type=click.Path())
@click.argument("filename", type=click.Path(exists=True))
@click.argument("tags", type=click.STRING)
def add_tag(vault, filename, tags):

    vault_ = load_vault(vault)

    vault_[filename] |= parse_tags(tags)

    save_vault(vault, vault_)


@cli.command()
@click.argument("vault", type=click.Path())
@click.option(
    "-t",
    "tags",
    type=click.STRING,
    multiple=True,
    required=True,
    help="Each instance of -t is considered an AND condition, which is then OR'd with others",
)
def ls(vault, tags):
    vault_ = load_vault(vault)

    tag_groups = [parse_tags(ts) for ts in tags]

    for file, tags_ in vault_.items():
        if any(t.issubset(tags_) for t in tag_groups):
            click.echo(file)


if __name__ == "__main__":
    cli()
