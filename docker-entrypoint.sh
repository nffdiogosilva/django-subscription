#!/bin/bash
set -e

# FIXME: In future, run bootstrap project only once
# TODO: In future run createsuperuser --email admin@exameple.com --username admin (but only once)
bootstrap_project() {
    cd $WORKDIR && \
    python manage.py migrate && \
    python manage.py check
}

bootstrap_project

exec "$@"
