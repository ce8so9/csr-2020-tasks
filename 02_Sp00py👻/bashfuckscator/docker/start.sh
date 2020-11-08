#!/bin/sh

mkdir /dev/tmp
chmod 703 /dev/tmp
exec su http -c '/usr/bin/socat tcp-l:2946,reuseaddr,fork EXEC:"timeout 15 /bashfuckscator.sh"'
