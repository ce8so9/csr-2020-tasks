FROM alpine:latest

RUN apk update && apk add socat qemu-system-x86_64 mtools dosfstools

ADD disk.qcow2 /disk.qcow2
ADD qemu.sh /qemu.sh
ADD entrypoint.sh /entrypoint.sh

RUN adduser -D -s /bin/bash app
USER app
ENTRYPOINT ["/entrypoint.sh"]
