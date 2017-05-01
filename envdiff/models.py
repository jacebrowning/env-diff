import re
import logging
from pathlib import Path
from contextlib import suppress

import yorm
from yorm.types import String, List, AttributeDictionary
import delegator


log = logging.getLogger(__name__)


class Variable:

    RE_ENV_SET = re.compile(r"""
        (?: export\  )?         # optional export call
        (?P<name> [A-Z_]+ )     # capitals and underscores
        =                       # equals sign
        (?P<value> .* )         # any value
    """, re.VERBOSE)

    RE_QUOTED_CAPITALS = re.compile(r"""
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

    def __eq__(self, other):
        for attr in {'name', 'value', 'context'}:
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True

    def __lt__(self, other):
        return self.name < other.name

    @classmethod
    def from_env(cls, line):
        line = line.strip()
        if not line:
            log.debug("Skipped blank line")
            return None

        if '=' not in line:
            log.info("Skipped line without key-value: %r", line)
            return None

        name, value = line.split('=', 1)
        if not name:
            log.info("Skipped line without key: %r", line)
            return None

        variable = cls(name, value=value)
        log.info("Loaded variable: %s", variable)

        return variable

    @classmethod
    def from_code(cls, *lines, index=0):
        line = lines[index].strip()

        match = (cls.RE_ENV_SET.match(line) or
                 cls.RE_QUOTED_CAPITALS.search(line))
        if not match:
            log.debug("Skipped line %s without variable: %r", index + 1, line)
            return None

        name = match.group('name')
        context = line
        with suppress(IndexError):
            if context.endswith('{'):
                context += lines[index + 1].strip()
                context += lines[index + 2].strip()

        variable = cls(name, context=context)
        log.info("Loaded variable: %s", variable)

        return variable


@yorm.attr(path=String)
class SourceFile(AttributeDictionary):

    def __init__(self, path=None, variables=None):
        super().__init__()
        self.path = path
        self.variables = variables or []

    def __str__(self):
        return f"File: {self.path}"

    def fetch(self):
        self.variables.clear()
        with Path(self.path).open() as file:
            lines = file.readlines()
        for index in range(len(lines)):
            variable = Variable.from_code(*lines, index=index)
            if variable:
                self.variables.append(variable)


@yorm.attr(name=String)
@yorm.attr(command=String)
class Environment(AttributeDictionary):

    def __init__(self, name=None, command="env", variables=None):
        super().__init__()
        self.name = name
        self.command = command
        self.variables = variables or []

    def __str__(self):
        return f"Environment: {self.name}"

    def fetch(self):
        self.variables.clear()
        result = delegator.run(self.command)
        for line in result.out.splitlines():
            variable = Variable.from_env(line)
            if variable:
                self.variables.append(variable)


@yorm.attr(sourcefiles=List.of_type(SourceFile))
@yorm.attr(environments=List.of_type(Environment))
@yorm.sync("{self.root}/{self.filename}", auto_create=False, auto_save=False)
class Config(yorm.ModelMixin):

    def __init__(self, filename="env-diff.yml", root=None,
                 sourcefiles=None, environments=None):
        self.root = root or Path.cwd()
        self.filename = filename
        self.sourcefiles = sourcefiles or []
        self.environments = environments or []

    def __str__(self):
        return str(self.path).replace('\\', '/')

    @property
    def path(self):
        return Path(self.root, self.filename)

    @property
    def variables(self):
        for container in self.sourcefiles + self.environments:
            for variable in container.variables:
                yield variable
