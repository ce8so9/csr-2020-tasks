FROM alpine:latest

RUN apk update && apk add socat bash file mailcap curl coreutils gcc musl-dev

ADD flag.txt /flag.txt
ADD get_flag.c /get_flag.c
ADD get_flag.sh /get_flag.sh
ADD start.sh /start.sh
ADD bashfuckscator.sh /bashfuckscator.sh

RUN gcc -static -o /get_flag /get_flag.c; \
    chown root: /flag.txt; \
    chmod 000 /flag.txt; \
    chmod 000 /start.sh; \
    chown root: /get_flag; \
    chmod a+sx /get_flag; \
    adduser -D -s /bin/bash http; \
    rmdir /tmp; \
    ln -s /dev/tmp /tmp

ENTRYPOINT ["/bin/sh", "/start.sh"]
