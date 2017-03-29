# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,singleton-comparison

from expecter import expect

from envdiff import utils


def describe_init_config():

    def it_sets_sample_data(tmpdir):
        tmpdir.chdir()

        config, created = utils.init_config()

        expect(created) == True
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

    def it_leaves_existing_files_alone(tmpdir):
        tmpdir.chdir()
        with open("env-diff.yml", 'w') as config_text:
            config_text.write("files: ['foo.bar']")

        config, created = utils.init_config()

        expect(created) == False
        expect(config.__mapper__.data) == dict(
            files=[
                "foo.bar",
            ],
        )
