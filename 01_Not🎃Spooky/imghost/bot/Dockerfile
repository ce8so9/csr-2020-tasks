FROM debian:buster

RUN apt-get -qq update && apt-get -qqy install python3-selenium python3-requests chromium chromium-driver

RUN addgroup --gid 1000 --system bot && adduser --system --uid 1000 --gid 1000 bot

ADD checker.py /home/bot/checker.py
ADD checker.sh /home/bot/checker.sh
USER bot

ENTRYPOINT /home/bot/checker.sh
