from pathlib import Path

import yorm
from yorm.types import String, List, AttributeDictionary


@yorm.attr(name=String)
@yorm.attr(command=String)
class Environment(AttributeDictionary):

    def __init__(self, name, command="env"):
        super().__init__()
        self.name = name
        self.command = command


@yorm.attr(files=List.of_type(String))
@yorm.attr(environments=List.of_type(Environment))
@yorm.sync("{self.root}/{self.filename}", auto_create=False)
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
