# Attacker (Mitnick's machine). network_mode: host + privileged: true in
# docker-compose.yml put this container in the host's own network
# namespace, so it can capture on the Docker bridge device itself and see
# traffic between xterminal and trustedserver as if it were on a hub --
# that bridge-capture trick is the whole reason this lab works at all.
# See topology.yml for why that only works inside one VM.
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
        python3 python3-pip \
        rsh-redone-client \
        tcpdump nmap iproute2 net-tools bridge-utils iputils-ping \
    && pip3 install scapy \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /volumes
CMD ["sleep", "infinity"]
