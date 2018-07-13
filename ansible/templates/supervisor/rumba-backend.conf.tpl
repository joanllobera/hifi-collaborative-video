[program:rumba-backend]
command={{ rumba_src_folder }}/rumba/backend/venv/bin/python api/api_controller.py
directory={{ rumba_src_folder }}/rumba/backend/
autostart=true
autorestart=true
startretries=3
stderr_logfile=/var/rumba/logs/rumba-back.err.log
stdout_logfile=/var/rumba/logs/rumba-back.out.log
user={{ ubuntu_user }}
