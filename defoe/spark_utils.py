"""
Spark-related file-handling utilities.
"""

HTTP = "http://"
HTTPS = "https://"
BLOB = "blob:"


def files_to_rdd(context,
                 num_cores=1,
                 data_file="data.txt"):
    """
    Populate Spark RDD with file names or URLs over which a query is
    to be run.

    :param context: Spark Context
    :type context: pyspark.context.SparkContext
    :param num_cores: number of cores over which to parallelize Spark
    job
    :type num_cores: int
    :param data_file: name of file with file names or URLs, one per
    line
    :type data_file: str or unicode
    :return: RDD
    :rtype: pyspark.rdd.RDD
    """
    filenames = [filename.strip() for filename in list(open(data_file))]
    rdd_filenames = context.parallelize(filenames, num_cores)
    return rdd_filenames



def files_to_dataframe(context,
                 num_cores=1,
                 data_file="data.txt"):
    """
    Populate Spark RDD with file names or URLs over which a query is
    to be run.

    :param context: Spark Context
    :type context: pyspark.context.SparkContext
    :param num_cores: number of cores over which to parallelize Spark
    job
    :type num_cores: int
    :param data_file: name of file with file names or URLs, one per
    line
    :type data_file: str or unicode
    """
    

    filenames = [filename.strip() for filename in list(open(data_file))]
    rdd_filenames = context.parallelize(filenames, num_cores)
    return rdd_filenames



def open_stream(filename):
    """
    Open a file and return a stream to the file.

    If filename starts with "http:" or "https:" then file is assumed
    to be a URL.

    If filename starts with "blob:" then file is assumed to be held
    within Azure as a BLOB. This expects the following environment
    variables to be set:

    * BLOB_SAS_TOKEN
    * BLOB_ACCOUNT_NAME
    * BLOB_CONTAINER_NAME

    Otherwise, the filename is assumed to be held on the file
    system.

    :param filename: file name or URL
    :type filename: str or unicode
    :return: open stream
    :rtype: cStringIO.StringI (URL or file system) OR io.BytesIO (blob)
    """
    assert filename, "Filename must not be ''"

    is_url = (filename.lower().startswith(HTTP) or
              filename.lower().startswith(HTTPS))
    is_blob = (filename.lower().startswith(BLOB))

    if is_url:
        import requests
        from io import StringIO

        stream = requests.get(filename, stream=True).raw
        stream.decode_content = True
        stream = StringIO(stream.read())

    elif is_blob:
        import io
        import os
        from azure.storage.blob import BlobService

        sas_token = os.environ['BLOB_SAS_TOKEN']
        if sas_token[0] == '?':
            sas_token = sas_token[1:]

        blob_service = BlobService(
            account_name=os.environ['BLOB_ACCOUNT_NAME'],
            sas_token=sas_token)
        filename = filename[len(BLOB):]
        blob = blob_service.get_blob_to_bytes(
            os.environ['BLOB_CONTAINER_NAME'],
            filename)
        stream = io.BytesIO(blob)

    else:
        stream = open(filename, 'rb')

    return stream
