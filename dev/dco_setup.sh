#!/bin/bash

# ============================================
# Script Name : dco_setup.sh
# Description : Sets up DCO sign-off (Signed-off-by: $name <$email>)
# Usage       : ./dco_setup.sh "Your Name" "your@email.com"
# ============================================

set -euo pipefail

# Get the directory of the current script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Ensure both name and email are provided
if [[ $# -ne 2 ]]; then
    echo "Usage: $0 \"Your Name\" \"your@email.com\""
    exit 1
fi

name="$1"
email="$2"

# Make dco_echo.sh executable
chmod +x "$DIR/dco_echo.sh"

# Set local git config
git config --local user.name "$name"
git config --local user.email "$email"

# Output confirmation
echo "DCO Identity Set:"
echo "   user.name  = $(git config --local user.name)"
echo "   user.email = $(git config --local user.email)"

# Call dco_echo.sh
"$DIR/dco_echo.sh"