[program:janus]
command={{ janus_dir }}/bin/janus
autostart=true
autorestart=true
startretries=3
stderr_logfile=/var/log/janus/janus.err.log
stdout_logfile=/var/log/janus/janus.out.log
user={{ ubuntu_user }}
