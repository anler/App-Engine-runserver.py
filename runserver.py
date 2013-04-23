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

import google


match = re.search(r'appengine_(\d\.\d\.(\d))', google.__path__[0])
gae_version = match.group(1)
minor_version = int(match.group(2))

_formatter = argparse.RawDescriptionHelpFormatter

base = os.path.join(os.path.dirname(__file__), 'stores')

storage = "{{base}}/{version}/{{namespace}}".format(version=gae_version)

if minor_version < 6:
    cmd = ("dev_appserver.py "
           "--skip_sdk_update_check "
           "--use_sqlite "
           "--enable_console "
           "--debug "
           "--address=0.0.0.0 --port=8000 "
           "--blobstore_path={storage}/application.blobstore "
           "--datastore_path={storage}/application.datastore "
           "--history_path={storage}/applation.datastore.history "
           "--logs_path={storage}/application.logs "
           "--search_indexes_path={storage} "
           "--disable_static_caching "
           "--high_replication "
           "--show_mail_body "
           "{extra_argv} .")
else:
    cmd = ("dev_appserver.py "
        # "--use_mtime_file_watcher "
        "--log_level debug "
        "--host=0.0.0.0 --port=8080 --admin_host=0.0.0.0 --admin_port=8083 "
        "--api_port=8084 --show_mail_body --enable_task_running yes "
        "--storage_path={storage} {extra_argv} .")

def mkdir_p(path):
    if os.path.isfile(path):
        path = os.path.dirname(path)
    if not os.path.exists(path):
        os.makedirs(path)


def run_appserver(namespace, server_argv=None):
    if server_argv is None:
        server_argv = []

    storage_path = storage.format(base=base, namespace=namespace)
    mkdir_p(storage_path)

    extra_args = " ".join(server_argv)
    command = cmd.format(storage=storage_path, extra_argv=extra_args)

    print("Running {0!r}".format(command))

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

    return run_appserver(args.namespace, server_argv)


if __name__ == "__main__":
    sys.exit(main())
