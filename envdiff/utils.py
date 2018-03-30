import csv

import log

from .models import Config, SourceFile, Environment


def init_config():
    """Generate a configuration file with sample data."""
    config = find_config()
    if config:
        log.info(f"Config file already exists: {config.path}")
        return config, False

    log.info("Generating config file...")
    config = Config.new()

    config.sourcefiles = [
        SourceFile("app.json"),
        SourceFile(".env"),
    ]
    config.environments = [
        Environment("localhost"),
        Environment("production", command="heroku run env"),
    ]

    config.save()

    return config, True


def find_config():
    config = Config.find()

    return config


def generate_table(config):
    containers = config.sourcefiles + config.environments

    header = ['Variable'] + [str(x) for x in containers]
    yield header

    keys = set()
    for container in containers:
        for variable in container.variables:
            keys.add(variable.name)

    for key in sorted(keys):
        row = [key]
        for container in containers:
            for variable in container.variables:
                if variable.name == key:
                    row.append(variable.context or variable.value)
                    break  # TODO: what if the variable appears multiple times?
            else:
                row.append('')
        yield row


def translate_markdown(rows):
    for index, row in enumerate(rows):
        yield '| ' + ' | '.join(row) + ' |'
        if index == 0:
            yield '| ' + ' | '.join(['---'] * len(row)) + ' |'


def write_markdown(rows, path):
    log.info("Writing to %s", path)
    with path.open('w') as file:
        for row in translate_markdown(rows):
            file.write(row + '\n')


def write_csv(rows, path):
    log.info("Writing to %s", path)
    with path.open('w') as file:
        csvfile = csv.writer(file, lineterminator='\n')
        for row in rows:
            csvfile.writerow(row)
