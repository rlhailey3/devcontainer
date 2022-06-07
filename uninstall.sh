#!/usr/bin/bash

LOCAL_BIN=~/.local/bin
if [ -d "$LOCAL_BIN" ]; then
    rm $LOCAL_BIN/dev-enter
    rm $LOCAL_BIN/dev-create
    rm $LOCAL_BIN/dev-rm
fi


