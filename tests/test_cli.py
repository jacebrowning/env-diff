# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,singleton-comparison

import pytest
from expecter import expect

from click.testing import CliRunner

from envdiff.cli import main


@pytest.fixture
def runner():
    return CliRunner()


def describe_cli():

    def describe_init():

        def when_config_missing(runner, tmpdir):
            tmpdir.chdir()

            result = runner.invoke(main, ['--init'])

            expect(result.output) == (
                "Generated config file: {}/env-diff.yml\n".format(tmpdir) +
                "Edit this file to match your application\n"
            )
            expect(result.exit_code) == 0

    def describe_run():

        def when_config_missing(runner, tmpdir):
            tmpdir.chdir()

            result = runner.invoke(main, [])

            expect(result.output) == \
                "No config file found, generate one with '--init'\n"
            expect(result.exit_code) == 1
