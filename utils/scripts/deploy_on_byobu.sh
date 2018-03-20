#!/usr/bin/env bash

byobu new-session -d -s $USER

byobu rename-window -t $USER:0 'BACKEND'
byobu send-keys "cd ~/code/rumba/backend && source venv/bin/activate && python api/api_controller.py" C-m

