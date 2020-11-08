FROM alpine:3.10.3

RUN apk update && apk add nginx nginx-mod-stream nginx-mod-http-headers-more php7 php7-openssl php7-sqlite3 php7-phar php7-fpm php7-mysqli php7-curl php7-snmp php7-session php7-json php7-pdo php7-opcache php7-ldap php7-gd php7-imap php7-xml php7-brotli php7-bz2 php7-pecl-imagick imagemagick supervisor
ADD etc/ /etc/
ADD srv/ /srv/
ENV TMPDIR /dev/shm
ENTRYPOINT ["/usr/bin/supervisord", "-n"]

