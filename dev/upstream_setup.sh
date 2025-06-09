#!/bin/bash

# ============================================
# Script Name : add_upstream_setup.sh
# Description : Add pyIPCS GitHub as upstream.       
# Usage       : ./add_upstream_setup.sh
# ============================================

set -euo pipefail

REMOTE_URL=https://github.com/ambitus/pyIPCS.git

if git remote get-url upstream &>/dev/null; then
    git remote set-url upstream "$REMOTE_URL"
else
    git remote add upstream "$REMOTE_URL"
fi

# Validate upstream
echo
echo "Remote 'upstream' is set to:"
echo
git remote get-url upstream
echo
