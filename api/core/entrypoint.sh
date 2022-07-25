#!/bin/sh
gunicorn -k uvicorn.workers.UvicornH11Worker -c core/gunicorn.py main:app
exec "$@"


