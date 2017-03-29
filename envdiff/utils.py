import logging

import yorm

from .models import Config, Environment


log = logging.getLogger(__name__)


def init_config():
    """Generate a configuration file with sample data."""
    config = find_config()
    if config:
        log.info(f"Config file already exists: {config.path}")
        return config, False

    log.info("Generating config file...")
    config = yorm.create(Config)

    config.files = ["app.json", ".env"]
    config.environments = [
        Environment("localhost"),
        Environment("production", command="heroku run env"),
    ]

    return config, True


def find_config():
    config = yorm.find(Config)

    return config
