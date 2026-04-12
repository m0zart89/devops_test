#!/bin/bash
set -e

echo "Starting App Container..."

bash /app/init.sh

echo "Application started"
exec python app.py