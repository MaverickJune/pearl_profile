#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Usage: $0 <script_name>"
  echo "Example: $0 tree_decoding (without .py extension)"
  exit 1
fi

SCRIPT_NAME=$1

# Execute the script as a Python module
python -m dev_tests.$SCRIPT_NAME
echo "Launched dev_tests.$SCRIPT_NAME"
