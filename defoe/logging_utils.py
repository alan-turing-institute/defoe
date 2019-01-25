"""
Logging-related utilities
"""

import logging
import logging.config
import os
import os.path
import yaml


LOG_PROPERTIES_FILE = "log.properties.yml"


def configure_logging():
    """
    Configure Python logging from a configuration file.
    If log.properties.yml exists then load it and use it to configure
    Python logging.

    For configuration properties, see: Python logging configuration
    https://docs.python.org/2/library/logging.config.html
    """
    if os.path.exists(LOG_PROPERTIES_FILE):
        with open(LOG_PROPERTIES_FILE, 'r') as f:
            config = yaml.safe_load(f)
        logging.config.dictConfig(config)


is_configured = False


def get_logger(name):
    """
    Gets current logger, configuring logger via a call to
    configure_logging() if logging has not yet been configured.

    :param name: name
    :type name: str or unicode
    :return: logger
    :rtype: logging.Logger
    """
    global is_configured
    if not is_configured:
        configure_logging()
        is_configured = True
    return logging.getLogger(name)
