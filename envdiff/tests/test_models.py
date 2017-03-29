# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,singleton-comparison

import pytest
from expecter import expect

from envdiff import models


def describe_config():

    @pytest.fixture
    def config():
        return models.Config.new(root="tmp/models", overwrite=True)

    def describe_str():

        def is_based_on_path(config):
            expect(str(config)) == "tmp/models/env-diff.yml"
