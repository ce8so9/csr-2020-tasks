FROM debian:buster

RUN apt update && apt-get install -y xinetd && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/

# challenge files
RUN useradd -m -s /bin/bash ctf
COPY bflol .
COPY flag.txt /
RUN chmod 711 bflol
COPY bflol_svc /etc/xinetd.d/

CMD xinetd -dontfork
