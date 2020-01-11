from click.testing import CliRunner
from wilfred.wilfred import cli


def test_basic():
    runner = CliRunner()
    result = runner.invoke(cli)

    assert result.exit_code == 0


def test_path():
    runner = CliRunner()
    result = runner.invoke(cli, "--version")

    assert result.exit_code == 0
