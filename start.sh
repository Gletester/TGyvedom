#!/bin/bash
# Start script for Railway
cd "$(dirname "$0")"
gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 2 --timeout 120 main:app
