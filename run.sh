#!/bin/bash

pip install xgs/ > /dev/null 2>&1

python3 src/main.py $@
