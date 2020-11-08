accesslog = "-"
access_log_format = (
    '%({X-Forwarded-For}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
)
bind = "0.0.0.0:22000"
keepalive = 60
worker_class = "gevent"
workers = 1