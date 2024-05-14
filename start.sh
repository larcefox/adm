#!/bin/bash

timestamp=$(date +%s)
file1="$PWD/src/dinamo/base_model.py"
# file2=$PWD"/db_models/"$timestamp"_model.py"
sqlacodegen --schemas config postgresql://postgres:rtlnd33g7a@212.42.38.234:32769/3db > $file1
echo 'DB export done'
