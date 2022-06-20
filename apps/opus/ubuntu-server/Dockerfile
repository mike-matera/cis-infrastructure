FROM docker.io/ubuntu:22.04 

RUN apt update -y && DEBIAN_FRONTEND=noninteractive apt install -y ubuntu-server sudo iputils-ping podman python3-pip curl git openssh-server zsh 

STOPSIGNAL SIGRTMIN+3
ENTRYPOINT [ "/sbin/init" ] 
