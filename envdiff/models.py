import re
import logging
from pathlib import Path

import yorm
from yorm.types import String, List, AttributeDictionary
import delegator


log = logging.getLogger(__name__)


class Variable:

    CAPITALS = re.compile("""
        (?: ['"] )          # any quote mark
        (?P<name> [A-Z_]+ ) # capitals and underscores
        (?: ['"] )          # any quote mark
    """, re.VERBOSE)

    def __init__(self, name, *, value=None, context=None):
        assert name
        self.name = name
        self.value = value
        self.context = context

    def __repr__(self):
        return f"<variable: {self}>"

    def __str__(self):
        if self.value:
            return f"{self.name}={self.value}"
        else:
            return f"{self.name} @ {self.context!r}"

    @classmethod
    def from_env(cls, line):
        line = line.strip()
        if not line:
            log.debug("Skipped blank line")
            return None

        if '=' not in line:
            log.info("Skipped line without variable: %r", line)
            return None

        name, value = line.split('=', 1)
        variable = cls(name, value=value)
        log.info("Loaded variable: %s", variable)

        return variable

    @classmethod
    def from_code(cls, line):
        line = line.strip()
        match = cls.CAPITALS.search(line)
        if not match:
            log.debug("Skipped line without variable: %r", line)
            return None

        name = match.group('name')
        variable = cls(name, context=line)
        log.info("Loaded variable: %s", variable)

        return variable


@yorm.attr(path=String)
class SourceFile(AttributeDictionary):

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.variables = []

    def __str__(self):
        return self.path

    @property
    def file(self):
        return Path(self.path).open()

    def fetch(self):
        self.variables = []
        with self.file as file:
            for line in file:
                variable = Variable.from_code(line)
                if variable:
                    self.variables.append(variable)


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


@yorm.attr(sourcefiles=List.of_type(SourceFile))
@yorm.attr(environments=List.of_type(Environment))
@yorm.sync("{self.root}/{self.filename}", auto_create=False, auto_save=False)
class Config(yorm.ModelMixin):

    def __init__(self, filename="env-diff.yml", root=None):
        self.root = root or Path.cwd()
        self.filename = filename
        self.sourcefiles = []
        self.environments = []

    def __str__(self):
        return str(self.path)

    @property
    def path(self):
        return Path(self.root, self.filename)
