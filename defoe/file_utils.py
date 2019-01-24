"""
Helper functions for accessing files within Python modules.
"""

import os


def get_path(module, *name):
    """
    Gets path to file in module, given module and relative path.

    :param module: module
    :type module: module
    :param *name: file name components
    :type *name: str or unicode
    :return: path to file
    :rtype: str or unicode
    """
    return os.path.join(os.path.dirname(module.__file__), *name)


def open_file(module, *name):
    """
    Gets path to file in module, given module and relative path,
    and returns open file.

    :param module: module
    :type module: module
    :param *name: file name components
    :type *name: str or unicode
    :return: file handle
    :rtype: file
    """
    return open(get_path(module, *name))


def load_content(module, *name):
    """
    Gets path to file in module, given module and relative path,
    and returns file content.

    :param module: module
    :type module: module
    :param *name: file name components
    :type *name: str or unicode
    :return: file content
    :rtype: str or unicode
    """
    with open_file(module, *name) as f:
        result = f.read()
    return result
