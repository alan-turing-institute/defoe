"""
Helper functions for accessing test files.
"""

import os


def get_path(*name):
    """
    Gets path to file relative to this module file.
    """
    return os.path.join(os.path.dirname(__file__), *name)


def open_file(*name):
    """
    Gets path to file relative to this module file and opens
    file.
    """
    return open(get_path(*name))


def load_content(*name):
    """
    Gets path to file relative to this module file, opens
    file and returns content.
    """
    with open_file(*name) as f:
        result = f.read()
    return result
