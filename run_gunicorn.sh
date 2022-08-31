#!/bin/bash

export DJANGO_SETTINGS_MODULE=blogsite.settings.prod
source .venv/bin/activate
gunicorn -c gunicorn.conf.py -D