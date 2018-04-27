#!/usr/bin/env bash

byobu new-session -d -s $USER

byobu rename-window -t $USER:0 'BACKEND'
byobu send-keys "cd ~/code/rumba/backend && source venv/bin/activate && python api/api_controller.py" C-m

byobu new-window -t $USER:1 -n 'FRONTEND'
byobu send-keys "cd ~/code/rumba/rumba-front && source ~/.nvm/nvm.sh && nvm use v7.8.0 && ng serve" C-m

byobu new-window -t $USER:2 -n 'JANUS'
byobu send-keys "/opt/janus/bin/janus" C-m
