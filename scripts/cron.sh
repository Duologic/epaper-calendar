#!/usr/bin/bash
set -euo pipefail

DIRNAME=$(dirname $0)
cd $DIRNAME/..
./.venv/bin/python main.py
