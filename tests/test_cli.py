from src import cli


def test_main(cli_runner):
    rv = cli_runner.invoke(cli.main, [])
    assert rv.exit_code == 0
    assert "Usage" in rv.output
