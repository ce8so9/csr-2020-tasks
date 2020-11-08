#!/bin/sh

sleep 10
echo "Starting bot"

cd /home/bot
while true; do
	timeout 30 python3 -u checker.py
	sleep 5
done
