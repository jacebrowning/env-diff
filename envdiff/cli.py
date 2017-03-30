import sys
import logging

import click
from crayons import green, yellow, red, cyan, magenta, white
import blindspin

from . import utils


log = logging.getLogger(__name__)


@click.command()
@click.option('--init', is_flag=True, help="Generate a sample config file.")
@click.option('-v', '--verbose', count=True)
def main(init=False, verbose=0):
    configure_logging(verbose)
    if init:
        do_init()
    else:
        do_run()


def do_init():
    config, created = utils.init_config()

    if created:
        click.echo(green("Generated config file: ") +
                   white(f"{config.path}", bold=True))
    else:
        click.echo(yellow("Config file already exists: ") +
                   white(f"{config.path}", bold=True))

    click.echo(cyan("Edit this file to match your application"))

    sys.exit(0)


def do_run():
    config = utils.find_config()

    if not config:
        click.echo(red("No config file found"))
        click.echo(cyan("Generate one with the '--init' command"))
        sys.exit(1)

    for sourcefile in config.sourcefiles:
        click.echo(magenta("Loading variables from source file: ") +
                   white(f"{sourcefile}", bold=True))
        with blindspin.spinner():
            sourcefile.fetch()
        print(sourcefile.variables)

    for environment in config.environments:
        click.echo(magenta("Loading variables from environment: ") +
                   white(f"{environment}", bold=True))
        with blindspin.spinner():
            environment.fetch()
        print(environment.variables)

    sys.exit(2)


def configure_logging(verbosity=0):
    if verbosity >= 2:
        level = logging.DEBUG
    elif verbosity >= 1:
        level = logging.INFO
    else:
        level = logging.WARNING

    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

    logging.getLogger('yorm').setLevel(logging.WARNING)


if __name__ == '__main__':  # pragma: no cover
    main()
