#!/bin/bash
export FLASK_APP=./guild-discovery/index.py

if [[ $1 == rebuildDatabase ]]; then
    flask refreshguilds
    echo "rebuilding database"
else
    echo "no rebuild requested"
fi

flask run --host=0.0.0.0