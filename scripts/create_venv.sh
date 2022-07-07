#!/bin/bash

python3.9 -m venv ~/envs/psychopy
source $HOME/envs/psychopy/bin/activate	
pip install -r requirements.txt\

echo created environment in $HOME/envs/psychopy
