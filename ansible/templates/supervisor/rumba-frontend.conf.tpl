[program:rumba-frontend]
command=/bin/bash -c "source ~/.nvm/nvm.sh && nvm use v7.8.0 && ng serve"
directory={{ rumba_src_folder }}/rumba/rumba-front
autostart=true
autorestart=true
startretries=3
stderr_logfile=/var/rumba/logs/rumba-front.err.log
stdout_logfile=/var/rumba/logs/rumba-front.out.log
user={{ ubuntu_user }}
