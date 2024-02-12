#!/bin/sh
# Use the PORT environment variable if it's set, default to 8100 otherwise
PORT=${PORT:-8080}
exec uvicorn app:app --host 0.0.0.0 --port $PORT
