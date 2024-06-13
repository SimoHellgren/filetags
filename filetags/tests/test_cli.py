from click.testing import CliRunner
from filetags.src.new_cli import cli


def test_ls(cli_runner: CliRunner):
    result = cli_runner.invoke(cli, ["ls"])

    assert result.output == "file1\nfile2\n"
