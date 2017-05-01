# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,singleton-comparison

import os
from contextlib import contextmanager

from expecter import expect

from envdiff import utils


@contextmanager
def inside(dirpath):
    cwd = os.getcwd()
    os.chdir(dirpath)
    try:
        yield
    finally:
        os.chdir(cwd)


def describe_init_config():

    def it_sets_sample_data(tmpdir):
        with inside(str(tmpdir)):

            config, created = utils.init_config()

            expect(created) == True
            expect(config.__mapper__.data) == dict(
                sourcefiles=[
                    dict(path="app.json"),
                    dict(path=".env"),
                ],
                environments=[
                    dict(name="localhost", command="env"),
                    dict(name="production", command="heroku run env"),
                ],
            )

    def it_leaves_existing_files_alone(tmpdir):
        with inside(str(tmpdir)):

            with open("env-diff.yml", 'w') as config_text:
                config_text.write("sourcefiles: [{path: 'foo.bar'}]")

            config, created = utils.init_config()

            expect(created) == False
            expect(config.__mapper__.data) == dict(
                sourcefiles=[
                    dict(path="foo.bar"),
                ],
            )
