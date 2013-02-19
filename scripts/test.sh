#!/usr/bin/env bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/..
cd $ROOT_DIR

echo '****Downloading and building dependencies****'
python -m unittest discover src/thehighseas/ -p '*test*.py'