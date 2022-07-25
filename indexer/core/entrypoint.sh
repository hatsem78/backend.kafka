#!/bin/sh
gunicorn -k uvicorn.workers.UvicornH11Worker -c gunicorn_conf.py main:app
exec "$@"


