# Cybersecurity game "The Mitnick Attack"

Linear game for [CyberRangeCZ Platform](https://docs.platform.cyberrange.cz/).
Structured on the `library-junior-hacker` sandbox/training template, content
based on SEED Labs' *Mitnick Attack Lab* (see ATTRIBUTION.txt — different,
more restrictive license than the template this repo is structured on).

## Game Levels Summary

- read the briefing and access the sandbox
- recognize the rsh trust relationship with `nmap`
- confirm the Trusted Server is silenced (simulated SYN flood) by sniffing
  a spoofed SYN's reply
- hijack a blind TCP session with Scapy to run a command on X-Terminal
- plant a permanent `.rhosts` backdoor and use it without spoofing

## Topology summary

| Host    | Image | Flavor  |
|---------|-------|---------|
| seed-vm | seed  | m1.large |
| router  | debian-12-x86_64 | m1.small |

Everything the attack itself needs lives **inside** `seed-vm` as three Docker
containers on an internal `10.9.0.0/24` network — see the design note at the
top of `topology.yml` for why this is one VM and not three. The CyberRangeCZ
topology's own network (`10.1.26.0/24`) is only there to reach `seed-vm`'s
console; students never interact with it directly.

| Container                | IP (inside seed-vm) | Role |
|---------------------------|----------------------|------|
| `attacker`                | host-mode networking | student's shell for the whole game |
| `xterminal-10.9.0.5`      | 10.9.0.5             | the target |
| `trustedserver-10.9.0.6`  | 10.9.0.6             | the impersonated, "silenced" trusted host |

## Before you deploy this

1. **Confirm the `seed` image name and `ubuntu` mgmt user** exist in your
   OpenStack catalog — this repo doesn't invent them, they're carried over
   from the buffer-overflow lab's working topology, but names drift between
   clouds.
2. **`community.docker.docker_compose_v2` must be installed on the Ansible
   control node** (`ansible-galaxy collection install community.docker`) —
   it isn't pulled by `requirements.yml` (that file is for *roles*, this is
   a *collection*).
3. **Outbound internet from seed-vm is required** at provisioning time
   (`apt-get`, Docker Hub pulls, `pip install scapy`) — confirm the router/WAN
   mapping in `topology.yml` actually gets seed-vm online before the
   `mitnick-lab` role runs.
4. **Tick "Generate variant sandboxes"** when creating the pool/training
   instance, or the two per-student flags (`flag_hijack`, `flag_backdoor`)
   will all come out identical and the anti-cheating point of having 30
   different flags is lost.
5. Build one sandbox and actually run the attack yourself before handing
   this to 30 students. The one thing this repo *can't* verify for you: that
   your specific OpenStack image has the kernel modules/sysctls needed for
   `privileged: true` + `network_mode: host` nested inside it (some locked-down
   cloud images disable this). If `conn1_spoof.py`/`conn2_spoof.py` sniff
   nothing at all even with a correct `IFACE`, this is the first thing to
   check.

## License

This repository uses **three** different licenses, not two — don't copy the
`library-junior-hacker` dual-license block verbatim without reading
ATTRIBUTION.txt:

- The Ansible/Docker/provisioning code in this repo: MIT.
- The `training.json` level structure and this README's framing: CC BY 4.0,
  following the `library-junior-hacker` template's own convention.
- **The attack's technical content (the scenario, the task breakdown, the
  Scapy restrictions, the exact rsh/handshake mechanics) is adapted from
  SEED Labs' Mitnick Attack Lab, which is CC BY-NC-SA 4.0** — Non-Commercial
  and Share-Alike. See ATTRIBUTION.txt. If your course/TP is non-commercial
  teaching, you're fine; if you plan to sell this training or a derivative
  of it, you need SEED Labs' permission first, and any redistribution of
  the content needs to carry the same CC BY-NC-SA terms.
