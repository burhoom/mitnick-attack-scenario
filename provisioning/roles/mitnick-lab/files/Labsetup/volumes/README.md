# Attacker scripts

- `probe_syn.py` — Level 3. Already works; read it before writing the rest.
- `conn1_spoof.py` — Level 4/5. Spoofs the client-initiated rsh connection.
- `conn2_spoof.py` — Level 4. Spoofs the second (error-channel) connection.

## Finding your capture interface

You are in `network_mode: host`, so `eth0` inside this container is the
*host's* interface, not the Docker bridge where xterminal/trustedserver
traffic actually flows. Find the bridge:

```
ip -brief addr show type bridge
brctl show
```

Look for the one on `10.9.0.0/24`. Put its name (looks like `br-xxxxxxxxxxxx`)
into the `IFACE` constant at the top of each script.

## The field restriction

To keep this close to what Mitnick could actually have known in 1994, your
spoofing logic may only act on, from a packet you sniffed:

- the TCP **sequence number** field — never the acknowledgment field,
- the TCP **flags** field,
- length fields (IP header length, IP total length, TCP header length).

If your code branches on `.ack` or on anything else from a captured packet,
you're using information a real off-path attacker wouldn't have.

## Order of operations

1. `python3 conn2_spoof.py &` (or in its own terminal) — it must already be
   listening.
2. `python3 conn1_spoof.py` — triggers the whole chain.
3. For the backdoor level: `python3 conn1_spoof.py --backdoor`, then once it
   succeeds, plain `rsh 10.9.0.5 cat flag_backdoor.txt` works with no
   password and no spoofing at all.
