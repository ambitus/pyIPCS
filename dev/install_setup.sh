#!/bin/bash

# ============================================
# Script Name : setup.sh
# Description : Sets up pyIPCS development enivronment.       
# Usage       : ./setup.sh
# ============================================

set -euo pipefail

echo "------------------------------------------"
echo "Setting Up pyIPCS Development Environment"
echo "------------------------------------------"
echo

# Get the directory of the current script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Make folder executable
find "$DIR/setup" -exec chmod +x {} \;

# Add setup to directory
DIR+="/setup"

echo "--------------------------------"
echo "Install Development Dependencies"
echo "--------------------------------"

pip install -r "$DIR/dev_requirements.txt"

echo "--------------------------------"
echo "Pre-Commit Setup"
echo "--------------------------------"

"$DIR/pre-commit_setup.sh"
