"""
Create Spark query job bundle.

    usage: create_job.py [-h] job data model query [config]

    Create Spark query job bundle

    positional arguments:
      job_dir     Directory to create to hold job bundle
      data        Data file listing data files to query
      model       Data model to which data files conform: ['books', 'papers']
      query       Python query file
      config      Query-specific configuration file

    optional arguments:
      -h, --help  show this help message and exit

The job bundle is structured as follows:

    <job_dir>/
        lwm/                 # Copy of lwm/ code, including...
        lwm/<model>/query.py # Copy of <query>
        lwm.zip              # ZIP of lwm/
        data.txt             # Copy of <data> file
        query.dat            # Copy of <config> file
"""

from argparse import ArgumentParser
import os
import shutil
import sys


def main():
    """
    Parses command-line arguments and creates job bundle.
    """
    module_dir = "lwm"
    data_file = "data.txt"
    query_file = "query.py"
    config_file = "query.dat"
    models = ["books", "papers"]

    parser = ArgumentParser(description="Create Spark query job bundle")
    parser.add_argument("job_dir",
                        help="Directory to create to hold job bundle")
    parser.add_argument("data",
                        help="Data file listing data files to query")
    parser.add_argument("model",
                        help="Data model to which data files conform: " +
                        str(models))
    parser.add_argument("query",
                        help="Python query file")
    parser.add_argument("config",
                        nargs="?",
                        default=None,
                        help="Query-specific configuration file")
    args = parser.parse_args()

    if args.model not in models:
        print(("model should be one of: " + str(models)))
        sys.exit(1)

    if os.path.exists(args.job_dir):
        if os.path.isdir(args.job_dir):
            shutil.rmtree(args.job_dir)
        else:
            os.remove(args.job_dir)
    os.mkdir(args.job_dir)

    shutil.copytree(module_dir,
                    os.path.join(args.job_dir, module_dir),
                    ignore=shutil.ignore_patterns("*.pyc",
                                                  "*__pycache__*",
                                                  "test"))

    shutil.copyfile(args.data, os.path.join(args.job_dir, data_file))
    shutil.copyfile(args.query,
                    os.path.join(args.job_dir,
                                 module_dir,
                                 args.model,
                                 query_file))
    if args.config:
        shutil.copyfile(args.config, os.path.join(args.job_dir, config_file))

    shutil.make_archive(os.path.join(args.job_dir, module_dir),
                        "zip",
                        os.path.join(args.job_dir),
                        os.path.join(module_dir))


if __name__ == "__main__":
    main()
