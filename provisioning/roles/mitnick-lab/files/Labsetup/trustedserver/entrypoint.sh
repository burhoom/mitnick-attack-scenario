#!/bin/bash
set -e

# --- Simulated SYN flood effect ---
# The real attack needs the Trusted Server's kernel to never see any
# unsolicited SYN+ACK sent to it, so it can't auto-RST and tear down the
# spoofed connection. Modern kernels can't actually be knocked over by a
# SYN flood the way 1994 ones could, so instead of fighting the kernel we
# just drop the one packet type that would give us away: incoming SYN+ACK.
# Everything else (ARP, legitimate inbound scans/connections) behaves
# completely normally, which is actually *more* faithful to "the Trusted
# Server's TCP stack never saw this handshake" than literally stopping
# the container would be.
iptables -A INPUT -p tcp --tcp-flags SYN,ACK SYN,ACK -j DROP

exec /usr/sbin/inetd -d /etc/inetd.conf
