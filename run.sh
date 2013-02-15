#!/usr/bin/env bash
set -e

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $ROOT_DIR

echo '****Entering environment****'
source bin/activate

echo '****Starting up****'
python src/server.py