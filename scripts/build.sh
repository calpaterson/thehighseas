#!/usr/bin/env bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/..
cd $ROOT_DIR

echo '****Checking for local depenencies****'
which python2
HAS_PYTHON2=$?
which pip
HAS_PIP=$?
which virtualenv
HAS_VIRTUALENV=$?
if [[ $HAS_PYTHON2 != 0 ]] || [[ $HAS_PIP != 0 ]] || [[ $HAS_VIRTUALENV != 0 ]]
then
    echo 'Not able to find python2, virtualenv or pip.  Make sure they are installed and on the $PATH'
    exit 1
fi

echo '****Building environment****'
virtualenv . --python=python2

echo '****Entering environment****'
source bin/activate

echo '****Downloading and building dependencies****'
pip install --use-mirrors -r scripts/requirements

touch .thehighseas-built