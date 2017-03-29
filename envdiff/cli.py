import logging

import click

from . import utils

log = logging.getLogger(__name__)


@click.command()
@click.option('--init', is_flag=True, help="Generate a sample config file.")
def main(init=False):
    logging.basicConfig(level=logging.INFO)

    if init:
        config = utils.init_config()
        click.echo(f"Created {config.path}")


if __name__ == '__main__':  # pragma: no cover
    main()
