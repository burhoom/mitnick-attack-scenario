# The Mitnick Attack

You are Mitnick. Two of your target's machines trust each other blindly: the
X-Terminal will run commands sent by the Trusted Server with no password at
all, because the two share an old-fashioned `.rhosts` trust relationship and
nobody double-checks more than a source IP address. You don't have the
Trusted Server's cooperation — but you don't need it. You just need it to
stay quiet while you borrow its identity.

## Disclaimer

This game is for educational purposes only. Unauthorized use of the attack
techniques in this game against systems you do not own or have explicit
permission to test is illegal. The game recreates a real, historical attack
(the 1994 Mitnick/Shimomura incident) for teaching purposes.

## License

Adapted from SEED Labs' *Mitnick Attack Lab* by Wenliang Du, licensed
CC BY-NC-SA 4.0. See ATTRIBUTION.txt. This derivative carries the same
license for its narrative/task content.

## Level 2: Recon: the trust relationship

**Learning outcome:** scan a network and identify a legacy, unauthenticated
remote-shell service by its port.

**Task assignment:** see `training.json`, level order 2.

**Estimated duration:** 5 minutes.

## Level 3: Confirm the Trusted Server is silenced

**Learning outcome:** understand *why* an attacker needs to silence a third
party before spoofing on its behalf — and prove, by sniffing, that a
silenced host's kernel can't interfere.

**Task assignment:** see `training.json`, level order 3.

**Estimated duration:** 10 minutes.

## Level 4: Hijack the connection

**Learning outcome:** complete a sniff-and-spoof program that blindly
completes a TCP three-way handshake and drives an application-layer protocol
(rsh) inside it, using only information a real off-path attacker could have
(sequence numbers, flags, lengths — never the acknowledgment field).

**Task assignment:** see `training.json`, level order 4.

**Estimated duration:** 25 minutes. This is the centerpiece task (10/20 pts).

## Level 5: Plant the backdoor

**Learning outcome:** understand persistence — why an attacker converts a
one-off exploit into a standing backdoor, and how trivially a single `+ +`
line in `.rhosts` achieves that here.

**Task assignment:** see `training.json`, level order 5.

**Estimated duration:** 13 minutes.
