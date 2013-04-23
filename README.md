# Google App Engine dev_appserver.py helper

Provides safe defaults when running dev_appserver.py

App Engine < 1.7.6

    --skip_sdk_update_check
    --use_sqlite
    --enable_console
    --debug
    --address=0.0.0.0 --port=[cmd line port]
    --blobstore_path=./stores/[app engine version]/[namespace]/application.blobstore
    --datastore_path=./stores/[app engine version]/[namespace]/application.datastore
    --history_path=./stores/[app engine version]/[namespace]/applation.datastore.history
    --logs_path=./stores/[app engine version]/[namespace]/application.logs
    --search_indexes_path=./stores/[app engine version]/[namespace]
    --disable_static_caching
    --high_replication
    --show_mail_body

App Engine >= 1.7.6

    --use_mtime_file_watcher
    --log_level debug
    --host=0.0.0.0 --port=8080
    --admin_host=0.0.0.0
    --show_mail_body
    --enable_task_running yes
    --storage_path=./stores/[app engine version]/[namespace]

## Usage

    python runserver.py [-h] port [namespace] -- [additional dev_appserver options]

## Examples

    python runserver.py 3000

    python runserver.py 3000 refactor

    python runserver.py 3000 -- --clear_datastore
