"""
Given a filename create a defoe.xml_directory.directory.Directory.
"""

from defoe.xml_directory.directory import Directory


def filename_to_object(filename):
    """
    Given a filename create a defoe.xml_directory.directory.Directory.
    If an error arises during its creation this is caught and returned
    as a string.

    :param filename: filename
    :type filename: str or unicode
    :return: tuple of form (Directory, None) or (filename, error message),
    if there was an error creating Directory
    :rtype: tuple(defoe.xml_directory.directory.Directory |
    str or unicode, str or unicode)
    """
    try:
        result = (Directory(filename), None)
    except Exception as exception:
        result = (filename, str(exception))
    return result
