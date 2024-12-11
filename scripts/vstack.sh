#!/bin/bash

source /venv/bin/activate
#emit sample/$1 | vstack -a=x64 -v $2 | carve printable -n 6
#echo "Running emit sample/$1 | vstack -v -a=x64 -W -c -L -s=$3 $2 | carve printable -n 9"
emit sample/$1 | vstack -v -a=x64 -W -c -L -s=$3 $2 | carve printable -n 5
