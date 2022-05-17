#!/bin/bash

SESSION="ide"

tmux new-session -d -s $SESSION
tmux split-window -v
tmux select-pane -t 0
tmux send-keys -t 0 "vim" C-m
tmux attach-session -t $SESSION:0
