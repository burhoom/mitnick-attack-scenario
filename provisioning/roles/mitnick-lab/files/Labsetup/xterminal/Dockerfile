# X-Terminal: the attack's target. Trusts the Trusted Server (10.9.0.6)
# for passwordless rsh/rlogin via .rhosts — the exact relationship Mitnick
# exploited against Shimomura's real machines in 1994.
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
        rsh-redone-server rsh-redone-client \
        openbsd-inetd \
        iproute2 net-tools iputils-ping \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash seed

# Baseline trust relationship (pre-attack state): X-Terminal trusts the
# Trusted Server's IP for passwordless rsh/rlogin. This file is what the
# attack ultimately overwrites with "+ +" in the backdoor task.
RUN echo "10.9.0.6" > /home/seed/.rhosts \
    && chown seed:seed /home/seed/.rhosts \
    && chmod 644 /home/seed/.rhosts

# Enable rshd (shell) and rlogind (login) under inetd, exactly as the
# SEED Lab manual describes for the rsh-redone packages.
RUN printf 'shell\tstream\ttcp\tnowait\troot\t/usr/sbin/in.rshd\tin.rshd -L\n' >> /etc/inetd.conf \
    && printf 'login\tstream\ttcp\tnowait\troot\t/usr/sbin/in.rlogind\tin.rlogind\n' >> /etc/inetd.conf

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 513 514
ENTRYPOINT ["/entrypoint.sh"]
