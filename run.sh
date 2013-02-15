#!/usr/bin/env bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $ROOT_DIR

REDIS_UP=`echo 'PING' | redis-cli | grep PONG`
if [[ $REDIS_UP != 0 ]]
then
    echo '!!!Redis is not up and running!!!'
    exit 1
fi

echo '****Entering environment****'
source bin/activate

echo '****Starting up****'
python src/server.py