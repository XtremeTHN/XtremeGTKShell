#!/bin/bash

cd xgs
python3 setup.py install > /dev/null 2>&1
cd ..

python3 src/main.py $@
