#!/bin/bash
source env/bin/activate

python3 -m doxypypy.doxypypy -a -c $1
