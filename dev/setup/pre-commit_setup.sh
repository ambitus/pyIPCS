#!/bin/bash

# ============================================
# Script Name : pre-commit_setup.sh
# Description : Install pre-commit hooks.       
# Usage       : ./pre-commit_setup.sh
# ============================================

set -euo pipefail

# Install default pre-commit stage
pre-commit install

# Install commit-msg hooks
pre-commit install --hook-type commit-msg