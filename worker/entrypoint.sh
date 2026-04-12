#!/bin/bash
set -e

mkdir -p /app/logs

exec python worker.py 2>&1 | tee /app/logs/worker.log