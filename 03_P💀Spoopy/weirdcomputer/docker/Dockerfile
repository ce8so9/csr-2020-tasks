FROM alpine:latest

RUN apk update && apk add socat python3

ADD emulator.py /emulator.py

RUN adduser -D -s /bin/bash app
USER app
ENTRYPOINT ["/usr/bin/socat", "tcp-l:2384,reuseaddr,fork", "EXEC:timeout 5 python3 /emulator.py"]
