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

        def when_config_missing(runner):
            result = runner.invoke(main, ['--init'])

            expect(result.exit_code) == 0
            expect(result.output) == "Created env-diff.yml\n"
