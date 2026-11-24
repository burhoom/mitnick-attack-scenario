#!/bin/bash
set -e
# openbsd-inetd needs to run in the foreground inside a container
exec /usr/sbin/inetd -d /etc/inetd.conf
