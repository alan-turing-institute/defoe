"""
Counts total number of directories.
"""


def do_query(directories, config_file=None, logger=None):
    """
    Iterate through directories and count total number of directories.
    Returns result of form:

        {"num_directories": num_directories}

    :param directories: RDD of defoe.xml_directory.directory.Directory
    :type directories: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file (unused)
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: total number of directories
    :rtype: dict
    """
    num_directories = directories.count()
    return {"num_directories": num_directories}
