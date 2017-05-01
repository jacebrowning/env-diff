# pylint: disable=redefined-outer-name,unused-argument,unused-variable,expression-not-assigned,singleton-comparison

import os
from pathlib import Path
from contextlib import suppress

import pytest
from expecter import expect

from click.testing import CliRunner

from envdiff.cli import main, do_run, do_report
from envdiff.models import Config, SourceFile, Environment


@pytest.fixture
def runner():
    return CliRunner()


@pytest.yield_fixture
def tmp():
    cwd = Path.cwd()
    dirpath = Path("tmp", "int", "cli").resolve()
    dirpath.mkdir(parents=True, exist_ok=True)
    os.chdir(dirpath)
    yield dirpath
    os.chdir(cwd)


def strip(tripple_quoted_string, *, indent):
    return tripple_quoted_string.strip().replace('    ' * indent, '') + '\n'


def describe_cli():

    def describe_init():

        def when_config_missing(runner, tmp):
            path = tmp.joinpath("env-diff.yml").resolve()
            with suppress(FileNotFoundError):
                print("Deleting {}".format(path))
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

    @pytest.yield_fixture
    def config(tmpdir):
        cwd = os.getcwd()
        tmpdir.chdir()

        with Path(".env").open('w') as f:
            f.write("FOO=1")

        with Path("app.py").open('w') as f:
            f.write("os.getenv('FOO', 2)")

        yield Config.new(
            sourcefiles=[
                SourceFile(".env"),
                SourceFile("app.py"),
            ],
            environments=[
                Environment("test", command="echo FOO=3"),
            ],
        )

        os.chdir(cwd)

    def it_returns_table_data(runner, config):
        print(config.sourcefiles)
        data = do_run(config)

        expect(list(data)) == [
            ['Variable', 'File: .env', 'File: app.py', 'Environment: test'],
            ['FOO', 'FOO=1', "os.getenv('FOO', 2)", '3'],
        ]


def describe_do_report():

    @pytest.fixture
    def rows():
        return [
            ['Foo', 'Bar'],
            ['', '42']
        ]

    def it_creates_md_and_csv(tmp, rows):
        do_report(rows)

        with tmp.joinpath("env-diff.md").open() as file:
            text = file.read()
            expect(text) == strip("""
            | Foo | Bar |
            | --- | --- |
            |  | 42 |
            """, indent=3)

        with tmp.joinpath("env-diff.csv").open() as file:
            text = file.read()
            expect(text) == strip("""
            Foo,Bar
            ,42
            """, indent=3)
