# Trusted Server: the machine Mitnick impersonated. Runs the same rsh
# service as X-Terminal, but boots permanently "silenced" (see
# entrypoint.sh) to simulate the effect of Mitnick's SYN flood without
# needing students to manually take it offline.
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
        rsh-redone-server rsh-redone-client \
        openbsd-inetd iptables \
        iproute2 net-tools iputils-ping \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash seed

RUN printf 'shell\tstream\ttcp\tnowait\troot\t/usr/sbin/in.rshd\tin.rshd -L\n' >> /etc/inetd.conf \
    && printf 'login\tstream\ttcp\tnowait\troot\t/usr/sbin/in.rlogind\tin.rlogind\n' >> /etc/inetd.conf

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 513 514
ENTRYPOINT ["/entrypoint.sh"]
