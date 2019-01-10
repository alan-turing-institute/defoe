"""
Module to load and parse a list of files into a Spark RDD
of Issues. This assumes that the files are stored on the
research data GPFS system which can be accessed over SSH
without any user interaction.
"""

from fs.sshfs import SSHFS

from newsrods.issue import Issue

# This is the URL of the research data GPFS
DATA_STORE_HOST = 'live.rd.ucl.ac.uk'


def get_streams(context, username, source='files.txt'):
    """
    Given a Spark Context, a username to the research data store GPFS
    which has passworldless ssh keys already set up, and a source file
    to read filenames from, load all the files from the RD GPFS and turn
    them into Issues. The Issues are returned as a Spark RDD
    """
    filenames = [filename.strip() for filename in list(open(source))]

    def filename_to_issue(filename):
        """
        Given a filename, load it from GPFS and parse it into an Issue
        """
        fs = SSHFS(host=DATA_STORE_HOST, user=username)
        stream = fs.open(filename, 'r', encoding='latin_1')
        issue = Issue(stream)
        stream.close()
        fs.close()
        return issue

    rdds = context.parallelize(filenames)
    issues = rdds.map(filename_to_issue)
    return issues
