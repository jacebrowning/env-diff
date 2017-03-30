# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,singleton-comparison

import pytest
from expecter import expect

from envdiff.models import Variable, SourceFile, Environment, Config


def describe_variable():

    @pytest.fixture
    def variable():
        return Variable('key', value="value")

    def describe_eq():

        def with_matching_key_and_value(variable):
            expect(variable) == Variable('key', value="value")

        def with_matching_key_and_different_value(variable):
            expect(variable) != Variable('key', value="foobar")

    def describe_from_env():

        def with_blank_line():
            expect(Variable.from_env(" ")) == None

        def without_equals():
            expect(Variable.from_env("foo bar")) == None

        def with_single_equals():
            expect(Variable.from_env("key=var")) == Variable('key', value="var")

        def with_single_equals_but_no_key():
            expect(Variable.from_env(" =value")) == None

        def with_single_equals_but_no_value():
            expect(Variable.from_env(" key= ")) == Variable('key', value="")

    def describe_from_code():

        def with_blank_line():
            expect(Variable.from_code(" ")) == None

        def with_no_caps_variable():
            expect(Variable.from_code("key=value")) == None

        def with_caps_variable():
            expect(Variable.from_code("let 'KEY'=value")) == \
                Variable('KEY', context="let 'KEY'=value")


def describe_sourcefile():

    @pytest.fixture
    def sourcefile():
        return SourceFile("tmp/app.json")

    def describe_str():

        def is_based_on_path(sourcefile):
            expect(str(sourcefile)) == "tmp/app.json"


def describe_environment():

    @pytest.fixture
    def environment():
        return Environment('staging')

    def describe_str():

        def is_based_on_name(environment):
            expect(str(environment)) == "staging"


def describe_config():

    @pytest.fixture
    def config():
        return Config.new(root="tmp/models", overwrite=True)

    def describe_str():

        def is_based_on_path(config):
            expect(str(config)) == "tmp/models/env-diff.yml"
