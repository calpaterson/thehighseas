#!/usr/bin/env bash
set -e

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/..
cd $ROOT_DIR

rm -rf bin/ include/ lib/ local/ share/ build/ .thehighseas-built