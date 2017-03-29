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
@yorm.sync("{self.path}")
class Config:

    def __init__(self, path="env-diff.yml"):
        self.path = path
