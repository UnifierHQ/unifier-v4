#!/bin/bash

FILEPATH="$(which python3)"

if [[ -z $FILEPATH ]]; then
  echo "Could not find a Python 3 installation."
  exit 1
fi

# shellcheck disable=SC2155
export PYTHONPATH=$(pwd)/src

python3 ./src/boot/bootloader.py "$@"
