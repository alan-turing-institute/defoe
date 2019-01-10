"""
Load and read files to get streams for Spark.
"""

from requests import get

from newsrods.issue import Issue


def open_stream(url):
    """
    Open stream for given URL.
    """
    stream = get(url, stream=True)  # requests.models.Response
    raw = stream.raw  # urllib3.response.HTTPResponse
    raw.decode_content = True
    return raw


def get_streams(context, num_cores=1,
                source="files.txt"):
    """
    Turn a list of filenames in a file into a RDD of Issue.

    If the first file starts with "http://" or "https://" then all
    files are assumed to be URLs, else all are assumed to be file
    paths.
    """
    filenames = [filename.strip() for filename in list(open(source))]
    are_urls = len(filenames) > 0 and \
        (filenames[0].lower().startswith("http://") or
         filenames[0].lower().startswith("https://"))
    rdd_filenames = context.parallelize(filenames, num_cores)
    if are_urls:
        issues = rdd_filenames.map(lambda url: open_stream(url)) \
                            .map(lambda raw: Issue(raw))
    else:
        issues = rdd_filenames.map(lambda file_name:
                                   Issue(file_name))
    return issues
