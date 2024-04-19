#!/bin/bash

tmux new-session -d -s mysession

tmux split-window -v

tmux resize-pane -t 0 -y 50

tmux send-keys -t 0 'venv/bin/python chat.py' C-m

tmux send-keys -t 1 'venv/bin/python send_to_chat.py' C-m

tmux attach-session -t mysession
