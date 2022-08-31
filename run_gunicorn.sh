#!/bin/bash

export DJANGO_SETTINGS_MODULE=blogsite.settings.prod
. .venv/bin/activate
gunicorn blogsite.wsgi:application -c gunicorn.conf.py -D