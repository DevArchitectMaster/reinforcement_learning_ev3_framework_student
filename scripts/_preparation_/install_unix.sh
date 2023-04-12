#!/bin/bash
set echo off

sudo -H pip3 install --upgrade pip

pip install -r requirements.txt

echo "."

read -p "Press any key to exit ..."