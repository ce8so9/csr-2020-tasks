FROM alpine:latest

RUN apk update && apk add socat bash file mailcap curl coreutils gcc musl-dev

ADD flag.txt /flag.txt
ADD get_flag.c /get_flag.c

RUN gcc -static -o /get_flag /get_flag.c && rm /get_flag.c; \
    chown root: /flag.txt; \
    chmod 000 /flag.txt; \
    chown root: /get_flag; \
    chmod a+sx /get_flag; \
    adduser -D -s /bin/bash http

ENTRYPOINT ["/usr/bin/socat", "tcp-l:9256,reuseaddr,fork", "SYSTEM:timeout 5 bash /site/site.sh"]
#ENTRYPOINT ["/usr/bin/socat", "tcp-l:9256,reuseaddr,fork", "SYSTEM:timeout 5 bash -x /site/site.sh"]

ADD site/ /site/
RUN cp /site/site.sh /site/static/source.txt
USER http
