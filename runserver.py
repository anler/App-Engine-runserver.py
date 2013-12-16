#!/usr/bin/env python
#
# Copyright (c) 2012 Floqq innovation SL. All Right Reserved
#
"""dev_appserver.py helper.

Additional arguments can be passed to dev_appserver.py separating them with a
"--", for example:
    python runserver.py -- --clear_datastore
"""
from __future__ import print_function
import os
import sys
import re
import subprocess
import argparse
import shlex

try:
    from colors import red, green
except ImportError:
    # pycolors not found
    red = green = lambda text: text


_formatter = argparse.RawDescriptionHelpFormatter

config = {
    'base': os.path.join(os.path.dirname(__file__), 'stores'),
    'storage': '{base}/{namespace}',
    'options': ['--show_mail_body']
}


def get_gae_version(version_file):
    """Get gae version dict."""
    with open(version_file) as f:
        version_line = f.readline()

    match = re.search(r'(?P<major>\d)\.(?P<minor>\d)\.(?P<build>\d)',
                      version_line)
    if match is None:
        raise ValueError("I cannot understand format of the release number")

    major_version = int(match.group('major'))
    minor_version = int(match.group('minor'))
    build_version = int(match.group('build'))

    return major_version, minor_version, build_version


def mkdir_p(path):
    if os.path.isfile(path):
        path = os.path.dirname(path)
    if not os.path.exists(path):
        os.makedirs(path)


def run_appserver(port, namespace, server_argv=None):
    if server_argv is None:
        server_argv = []

    storage_path = config['storage'].format(base=config['base'],
                                            namespace=namespace)
    mkdir_p(storage_path)

    options = config['options'][:]
    options.extend(server_argv)
    options = ' '.join(options).format(port=port, storage=storage_path)

    command = 'dev_appserver.py {options} .'.format(options=options)

    print(green("Running devappserver.py with options:"))
    print(green('\n'.join(options.split(' '))))

    return subprocess.call(command, shell=True)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if "--" in argv:
        index = argv.index("--")
        server_argv = argv[index + 1:]
        argv = argv[:index]
    else:
        server_argv = None
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("port", help="Port for the server to run on")
    parser.add_argument("namespace", default="default", nargs="?",
                        help=("Namespace in which store datastore, blobstore "
                              "and searchindex data. Defaults to 'default'"))
    args = parser.parse_args(argv)

    return run_appserver(args.port, args.namespace, server_argv)


if __name__ == "__main__":
    import google

    gae_version_path = os.path.join(google.__path__[0], '..', 'VERSION')
    major, minor, build = get_gae_version(gae_version_path)

    if build < 6:
        options = ["--skip_sdk_update_check",
                   "--use_sqlite",
                   "--enable_console",
                   "--debug",
                   "--address=0.0.0.0",
                   "--port={port}",
                   "--blobstore_path={storage}/application.blobstore",
                   "--datastore_path={storage}/application.datastore",
                   "--history_path={storage}/applation.datastore.history",
                   "--search_indexes_path={storage}",
                   "--disable_static_caching",
                   "--high_replication"]
        if build == 5:
            options.append("--logs_path={storage}/application.logs")
    else:
        options = ['--use_mtime_file_watcher',
                   '--log_level debug',
                   '--host=0.0.0.0 --port={port}',
                   '--admin_host=0.0.0.0',
                   '--enable_task_running yes',
                   '--storage_path={storage}']
        if build < 8:
            options.append('--backends')

    config['options'].extend(options)

    sys.exit(main())
