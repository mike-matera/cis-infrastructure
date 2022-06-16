FROM ubuntu:focal as main
RUN apt-get update -q -y && apt-get upgrade -y && DEBIAN_FRONTEND=noninteractive apt-get install -y -q bind9 python3-pip bind9-dnsutils
RUN rm -f /etc/bind/named.conf

RUN pip3 install pyyaml jinja2 pydig
COPY . /cis-dns

EXPOSE 53/udp 
WORKDIR /cis-dns
CMD ["/bin/sh", "./entrypoint.sh"]
