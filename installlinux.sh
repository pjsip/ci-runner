#!/bin/bash
# Note: this script may be run from user's root repo directory
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
pushd "$SCRIPT_DIR"

echo Installing gdb..
sudo apt-get -y -q install gdb
sudo `which python` linuxrunner.py -i

popd
