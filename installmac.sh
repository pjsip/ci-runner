#!/bin/bash
# Note: this script may be run from user's root repo directory

SCRIPT_DIR=$(dirname "$0")
pushd "$SCRIPT_DIR"

# There's nothing to install on Mac.
# - we use lldb (installed)
# - we use existing core pattern: '/cores/core.%P'

popd
