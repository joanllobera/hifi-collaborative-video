[program:rumba-frontend]
command=/bin/bash -c "source /home/{{ ubuntu_user }}/.nvm/nvm.sh && nvm use {{ node_version }} && ng serve --open --host 0.0.0.0 --port 4200 --poll=1000"
directory={{ rumba_src_folder }}/rumba/rumba-front
autostart=true
autorestart=true
startretries=3
stderr_logfile=/var/rumba/logs/rumba-front.err.log
stdout_logfile=/var/rumba/logs/rumba-front.out.log
user={{ ubuntu_user }}
