import logging

from .models import Config, Environment


log = logging.getLogger(__name__)


def init_config():
    """Generate a configuration file with sample data."""
    config = Config()

    config.files = ["app.json", ".env"]
    config.environments = [
        Environment("localhost"),
        Environment("production", command="heroku run env"),
    ]

    return config
