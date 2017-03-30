import logging
from pathlib import Path

import yorm
from yorm.types import String, List, AttributeDictionary
import delegator


log = logging.getLogger(__name__)


class Variable:

    def __init__(self, name, value):
        assert name
        self.name = name
        self.value = value

    def __repr__(self):
        return f"<variable: {self}>"

    def __str__(self):
        return f"{self.name}={self.value}"

    @classmethod
    def from_env(cls, line):
        line = line.strip()
        if not line:
            log.debug("Skipped blank line")
            return None

        if '=' not in line:
            log.info("Skipped line without '=': %r", line)
            return None

        name, value = line.split('=', 1)
        variable = cls(name, value)
        log.info("Loaded variable: %s", variable)

        return variable


@yorm.attr(name=String)
@yorm.attr(command=String)
class Environment(AttributeDictionary):

    def __init__(self, name, command="env"):
        super().__init__()
        self.name = name
        self.command = command
        self.variables = []

    def __str__(self):
        return self.name

    def fetch(self):
        self.variables = []
        result = delegator.run(self.command)
        for line in result.out.splitlines():
            variable = Variable.from_env(line)
            if variable:
                self.variables.append(variable)


@yorm.attr(files=List.of_type(String))
@yorm.attr(environments=List.of_type(Environment))
@yorm.sync("{self.root}/{self.filename}", auto_create=False, auto_save=False)
class Config(yorm.ModelMixin):

    def __init__(self, filename="env-diff.yml", root=None):
        self.root = root or Path.cwd()
        self.filename = filename
        self.files = []
        self.environments = []

    def __str__(self):
        return str(self.path)

    @property
    def path(self):
        return Path(self.root, self.filename)
