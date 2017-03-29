# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,singleton-comparison

from expecter import expect

from envdiff import utils


def describe_init_config():

    def it_sets_sample_data(tmpdir):
        tmpdir.chdir()

        config = utils.init_config()

        expect(config.__mapper__.data) == dict(
            files=[
                "app.json",
                ".env",
            ],
            environments=[
                dict(
                    name="localhost",
                    command="env",
                ),
                dict(
                    name="production",
                    command="heroku run env",
                ),
            ],
        )
