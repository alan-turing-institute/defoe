"""
Checks XML directories for any anomalies.
"""


def do_query(directories, config_file=None, logger=None):
    """
    Checks XML directories for any anomalies.

    Returns result of form:

        {
            "no_files": <EMPTY_DIRECTORIES>,
            "no_mets": <DIRECTORIES_WITH_NO_METS>,
            "multiple_mets": <DIRECTORIES_WITH_MULTIPLE_METS>,
            "multiple_prefixes": <DIRECTORIES_WITH_MULTIPLE_FILE_PREFIXES
        }

    :param directories: RDD of defoe.xml_directory.directory.Directory
    :type directories: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file (unused)
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: information on anomalies
    :rtype: dict
    """
    metadata = directories.map(lambda directory:
                               (directory.directory,
                                directory.files,
                                directory.mets,
                                list(directory.prefixes)))
    no_files = metadata.filter(lambda directory:
                               len(directory[1]) == 0)
    no_mets = metadata.filter(lambda directory:
                              len(directory[2]) == 0)
    multiple_mets = metadata.filter(lambda directory:
                                    len(directory[2]) > 1)
    multiple_prefixes = metadata.filter(lambda directory:
                                        len(directory[3]) > 1)
    no_files = no_files \
        .map(lambda directory: directory[0]) \
        .collect()
    no_mets = no_mets \
        .map(lambda directory: directory[0]) \
        .collect()
    multiple_mets = multiple_mets \
        .map(lambda directory: {directory[0]: directory[2]}) \
        .collect()
    multiple_prefixes = multiple_prefixes \
        .map(lambda directory: {directory[0]: directory[3]}) \
        .collect()
    return {
        "no_files": no_files,
        "no_mets": no_mets,
        "multiple_mets": multiple_mets,
        "multiple_prefixes": multiple_prefixes
    }
