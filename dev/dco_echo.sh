#!/bin/bash

# ============================================
# Script Name : dco_echo.sh
# Description : Displays example DCO signoff (Signed-off-by: $name <$email>).       
# Usage       : ./dco_echo.sh
# ============================================

set -euo pipefail

# Read Git identity
name=$(git config user.name || echo "")
email=$(git config user.email || echo "")

if [[ -z "$name" || -z "$email" ]]; then
  echo "Git user.name or user.email is not set."
  echo "Run:"
  echo "     git config --local user.name \"Your Name\""
  echo "     git config --local user.email \"you@example.com\""
  echo "Or Run:"
  echo "     ./dev/dco_setup.sh \"Your Name\" \"you@example.com\""
  exit 0
fi

# Print example signoff
echo
echo "Current DCO signoff:"
echo
echo "   Signed-off-by: $name <$email>"
echo