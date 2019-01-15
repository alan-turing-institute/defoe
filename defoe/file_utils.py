"""
File-handling utilities.
"""

HTTP = "http://"
HTTPS = "https://"
BLOB = "blob:"


def files_to_rdd(context,
                 num_cores=1,
                 data_file="data.txt"):
    """
    Populate Spark RDD with file names over which query is to be run.
    """
    filenames = [filename.strip() for filename in list(open(data_file))]
    rdd_filenames = context.parallelize(filenames, num_cores)
    return rdd_filenames


def open_stream(filename):
    """
    Open a file and return a stream.
    """
    assert filename, "Filename must not be ''"

    is_url = (filename.lower().startswith(HTTP) or
              filename.lower().startswith(HTTPS))
    is_blob = (filename.lower().startswith(BLOB))

    if is_url:
        import requests
        from cStringIO import StringIO

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

        blob_service = BlobService(account_name=os.environ['BLOB_ACCOUNT_NAME'],
                                   sas_token=sas_token)
        filename = filename[len(BLOB):]
        blob = blob_service.get_blob_to_bytes(os.environ['BLOB_CONTAINER_NAME'],
                                              filename)
        stream = io.BytesIO(blob)

    else:
        from cStringIO import StringIO
        stream = StringIO(open(filename).read())

    return stream
