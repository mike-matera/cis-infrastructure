FROM docker.io/ubuntu:22.04 

RUN apt update -y && DEBIAN_FRONTEND=noninteractive apt install -y \
    ubuntu-server sudo curl git python3-pip python3-venv

STOPSIGNAL SIGRTMIN+3
ENTRYPOINT [ "/sbin/init" ] 
