# pylint: disable=redefined-outer-name,unused-argument,unused-variable,expression-not-assigned,singleton-comparison

import os
from pathlib import Path
from contextlib import suppress

import pytest
from expecter import expect

from click.testing import CliRunner

from envdiff.cli import main, do_run
from envdiff.models import Config, SourceFile, Environment


@pytest.fixture
def runner():
    return CliRunner()


@pytest.yield_fixture
def tmp(path=Path("tmp", "int", "cli").resolve()):
    cwd = Path.cwd()
    path.mkdir(parents=True, exist_ok=True)
    os.chdir(path)
    yield path
    os.chdir(cwd)


def describe_cli():

    def describe_init():

        def when_config_missing(runner, tmp):
            path = tmp.joinpath("env-diff.yml")
            with suppress(FileNotFoundError):
                path.unlink()

            result = runner.invoke(main, ['--init'])

            expect(result.output) == (
                "Generated config file: {}\n".format(path) +
                "Edit this file to match your application\n"
            )
            expect(result.exit_code) == 0

    def describe_run():

        def when_config_missing(runner, tmp):
            path = tmp.joinpath("env-diff.yml")
            with suppress(FileNotFoundError):
                path.unlink()

            result = runner.invoke(main, [])

            expect(result.output) == (
                "No config file found\n" +
                "Generate one with the '--init' command\n"
            )
            expect(result.exit_code) == 1


def describe_do_run():

    @pytest.fixture
    def config(tmpdir):
        tmpdir.chdir()

        with Path(".env").open('w') as f:
            f.write("FOO=1")

        with Path("app.py").open('w') as f:
            f.write("os.getenv('FOO', 2)")

        return Config.new(
            sourcefiles=[
                SourceFile(".env"),
                SourceFile("app.py"),
            ],
            environments=[
                Environment("test", command="echo FOO=3"),
            ],
        )

    def it_returns_table_data(runner, config):
        print(config.sourcefiles)
        data = do_run(config)

        expect(list(data)) == [
            ['Variable', 'File: .env', 'File: app.py', 'Environment: test'],
            ['FOO', 'FOO=1', "os.getenv('FOO', 2)", '3'],
        ]
