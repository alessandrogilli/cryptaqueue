#!/bin/bash
set -e

sudo apt update
sudo apt install python3 python3-pip python3-venv tmux

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi;

source "venv/bin/activate"

pip install -r "requirements.txt"

deactivate
