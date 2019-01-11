"""
Helper functions for accessing test files.
"""

import os


def get_path(module, *name):
    """
    Gets path to file relative to a module file.
    """
    return os.path.join(os.path.dirname(module.__file__), *name)


def open_file(module, *name):
    """
    Gets path to file relative to a module file and opens
    file.
    """
    return open(get_path(module, *name))


def load_content(module, *name):
    """
    Gets path to file relative to a module file, opens
    file and returns content.
    """
    with open_file(module, *name) as f:
        result = f.read()
    return result
