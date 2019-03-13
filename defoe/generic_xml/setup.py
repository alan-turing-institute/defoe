"""
Given a filename create a defoe.generic_xml.document.Document.
"""

from defoe.generic_xml.document import Document


def filename_to_object(filename):
    """
    Given a filename create a defoe.generic_xml.document.Document. If
    an error arises during its creation this is caught and returned as
    a string.

    :param filename: filename
    :type filename: str or unicode
    :return: tuple of form (Document, None) or (filename, error message),
    if there was an error creating Document
    :rtype: tuple(defoe.generic_xml.document.Document | str or
    unicode, str or unicode)
    """
    try:
        result = (Document(filename), None)
    except Exception as exception:
        result = (filename, str(exception))
    return result
