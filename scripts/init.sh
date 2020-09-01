#!/bin/bash
set -euo pipefail

DIRNAME=$(dirname $0)
cd $DIRNAME/..
git submodule update --init
python -m venv .venv
CFLAGS="-fcommon" ./.venv/bin/pip install -r req.txt
