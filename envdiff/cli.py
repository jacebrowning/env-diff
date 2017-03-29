import sys
import logging

import click
from crayons import green, yellow, red, cyan, white

from . import utils


log = logging.getLogger(__name__)


@click.command()
@click.option('--init', is_flag=True, help="Generate a sample config file.")
@click.option('-v', '--verbose', count=True)
def main(init=False, verbose=0):
    configure_logging(verbose)

    if init:
        config, created = utils.init_config()
        if created:
            click.echo(green("Generated config file: ") +
                       white(f"{config.path}"))
        else:
            click.echo(yellow("Config file already exists: ") +
                       white(f"{config.path}"))
        click.echo(cyan("Edit this file to match your application"))
        sys.exit(0)

    config = utils.find_config()
    if not config:
        click.echo(red("No config file found, generate one with '--init'"))
        sys.exit(1)

    sys.exit(2)


def configure_logging(verbosity=0):
    if verbosity >= 2:
        level = logging.DEBUG
    elif verbosity >= 1:
        level = logging.INFO
    else:
        level = logging.WARNING
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


if __name__ == '__main__':  # pragma: no cover
    main()
