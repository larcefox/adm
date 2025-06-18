#!/bin/bash

timestamp=$(date +%s)
file1="$PWD/src/dinamo/base_model.py"
# file2=$PWD"/db_models/"$timestamp"_model.py"
sqlacodegen --schemas config postgresql://larce:Dronsy25@localhost:5432/adm > $file1
echo 'DB export done'
