"""
Counts total number of documents, pages and words per year.

This can be useful if wanting to see how the average number of
documents, pages and words change over time, for example.
"""


def do_query(archives, config_file=None, logger=None, context=None):
    """
    Iterate through archives and count total number of documents,
    pages and words per year.

    Returns result of form:

        {
          <YEAR>: [<NUM_DOCUMENTS>, <NUM_PAGES>, <NUM_WORDS>],
          ...
        }

    :param archives: RDD of defoe.nls.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file (unused)
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: total number of documents, pages and words per year
    :rtype: list
    """
    newdf=df.filter(df.page_string.isNotNull()).filter(df["year"]!="year").filter(df["model"]=="nls").select(df.year, df.archive_filename,df.num_pages,df.page_string)
    archive_df= newdf.groupby("archive_filename", "year","num_pages").count()
    #>>> archive_df.show()
    # +--------------------+----+---------+-----+
    # |    archive_filename|year|num_pages|count|
    # +--------------------+----+---------+-----+
    # |/mnt/lustre/at003...|1842|      810|  785|
    # |/mnt/lustre/at003...|1778|      886|  829|
    # |/mnt/lustre/at003...|1810|      446|  422|
    # |/mnt/lustre/at003...|1823|      878|  833|
    # +--------------------+----+---------+-----+

    # I need to take the number of words per page!
    #todo return result
