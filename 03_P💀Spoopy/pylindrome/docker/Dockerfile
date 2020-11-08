FROM alpine:latest

RUN apk update && apk add socat python3 sudo
RUN adduser -D -s /bin/false sandbox
ENTRYPOINT ["/usr/bin/socat", "tcp-l:7809,reuseaddr,fork", "EXEC:timeout 5 python3 /app.py"]

ADD flag.txt /flag.txt
RUN chown root:root /flag.txt && chmod 000 /flag.txt
ADD app.py /app.py
