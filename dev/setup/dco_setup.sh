#!/bin/bash

# ============================================
# Script Name : dco_setup.sh
# Description : Sets up DCO sign-off (Signed-off-by: $name <$email>).
#               For git commits with -s parameter.       
# Usage       : ./dco_setup.sh
# ============================================

set -euo pipefail

# Get the directory of the current script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

while true; do
    echo 
    echo "Note: Sign-off should include your name and public GitHub email"
    "$DIR/dco_echo.sh"
    read -rp "Setup/Change Your DCO Sign-off For Commits? [Y/n]: " answer_setup
    answer_setup=${answer_setup:-y}

    if [[ "$answer_setup" =~ ^[Yy]$ ]]; then
        while true; do
            # Prompt for name and email
            read -r -p "Enter Your Name: " name
            read -r -p "Enter Public GitHub Account Email: " email

            # Apply as local config
            git config --local user.name "$name"
            git config --local user.email "$email"

            # Validate DCO setup
            echo
            echo "DCO Identity Set:"
            echo "   user.name  = $(git config --local user.name)"
            echo "   user.email = $(git config --local user.email)"

            # Call dco_echo.sh
            "$DIR/dco_echo.sh"

            read -rp "Do you want to re-enter your sign-off? [y/N]: " answer_redo
            answer_redo=${answer_redo:-n}

            if [[ "$answer_redo" =~ ^[Yy]$ ]]; then
                continue
            else
                exit 0
            fi
        done
    fi

    break
done
