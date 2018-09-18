[program:rumba-frontend]
command=/bin/bash -c "source /home/{{ ubuntu_user }}/.nvm/nvm.sh && nvm use {{ node_version }} && ng serve"
directory={{ rumba_src_folder }}/rumba/rumba-front
autostart=true
autorestart=true
startretries=3
stderr_logfile=/var/rumba/logs/rumba-front.err.log
stdout_logfile=/var/rumba/logs/rumba-front.out.log
user={{ ubuntu_user }}
