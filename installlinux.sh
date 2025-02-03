#!/bin/bash
# Note: this script may be run from user's root repo directory
sudo apt-get -y -q install gdb
sudo `which python` linuxrunner.py -i
