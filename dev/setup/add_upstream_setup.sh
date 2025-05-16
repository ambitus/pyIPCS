#!/bin/bash

# ============================================
# Script Name : add_upstream_setup.sh
# Description : Add pyIPCS GitHub as upstream.       
# Usage       : ./add_upstream_setup.sh
# ============================================

set -euo pipefail

REMOTE_URL=https://github.com/ambitus/pyIPCS.git

if git remote get-url upstream &>/dev/null; then
    echo "Remote 'upstream' already exists:"
    echo
    git remote get-url upstream
    echo

    read -rp "Do you want to replace it with '$REMOTE_URL'? [Y/n] " confirm
    confirm=${confirm:-y}  # Default to 'y' if empty

    if [[ "$confirm" =~ ^[Nn]$ ]]; then
        echo "Remote unchanged."
    else
        git remote set-url upstream "$REMOTE_URL"
    fi
else
    git remote add upstream "$REMOTE_URL"
fi

# Validate upstream
echo
echo "Remote 'upstream' is set to:"
echo
git remote get-url upstream
echo
