FROM docker.io/ubuntu:22.04 

# Un-minimize the system
RUN rm /etc/dpkg/dpkg.cfg.d/excludes && apt-get update -y
RUN dpkg -S /usr/share/man/ | sed 's|, |\n|g;s|: [^:]*$||' | DEBIAN_FRONTEND=noninteractive xargs apt-get install --reinstall -y
RUN dpkg --verify --verify-format rpm | awk '/..5......   \/usr\/share\/doc/ {print $2}' | sed 's|/[^/]*$||' | sort | uniq \
         | xargs dpkg -S | sed 's|, |\n|g;s|: [^:]*$||' | uniq | DEBIAN_FRONTEND=noninteractive xargs apt-get install --reinstall -y
RUN dpkg --verify --verify-format rpm | awk '/..5......   \/usr\/share\/locale/ {print $2}' | sed 's|/[^/]*$||' | sort | uniq \
         | xargs dpkg -S | sed 's|, |\n|g;s|: [^:]*$||' | uniq | DEBIAN_FRONTEND=noninteractive xargs apt-get install --reinstall -y
RUN rm -f /etc/update-motd.d/60-unminimize && \
    rm -f /usr/bin/man && \
    dpkg-divert --quiet --remove --rename /usr/bin/man

RUN apt update -y && DEBIAN_FRONTEND=noninteractive apt install -y \
    ubuntu-server sudo curl git python3-pip python3-venv podman

STOPSIGNAL SIGRTMIN+3
ENTRYPOINT [ "/sbin/init" ] 
