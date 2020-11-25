#!/bin/bash

if [[ $REBUILD_DATABASE == true ]]; then
    flask refreshguilds
    echo "rebuilding database"
else
    echo "no rebuild requested"
fi

python $FLASK_APP