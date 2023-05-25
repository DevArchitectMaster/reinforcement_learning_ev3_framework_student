#!/bin/bash
set echo off

cd "../../model_storage/"

find ./ -d -type d -exec rm -rf '{}' \;

echo "."

read -p "Press any key to exit ..."