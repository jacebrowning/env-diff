"""Unit tests configuration file."""

import log


def pytest_configure(config):
    """Disable verbose output when running tests."""
    log.init(level=log.DEBUG)
    log.silence('yorm', allow_warning=True)

    terminal = config.pluginmanager.getplugin('terminal')
    base = terminal.TerminalReporter

    class QuietReporter(base):
        """A py.test reporting that only shows dots when running tests."""

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.verbosity = 0
            self.showlongtestinfo = False
            self.showfspath = False

    terminal.TerminalReporter = QuietReporter
