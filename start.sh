#!/bin/bash

timestamp=$(date +%s)
file1="$PWD/src/dinamo/base_model.py"
# file2=$PWD"/db_models/"$timestamp"_model.py"
sqlacodegen --schemas config postgresql://mvp_user:mvp_pass@localhost:5432/3db > $file1
echo 'DB export done'
