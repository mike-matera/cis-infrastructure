FROM docker.io/ubuntu:22.04 

RUN apt update -y && DEBIAN_FRONTEND=noninteractive apt install -y ubuntu-server  

STOPSIGNAL SIGRTMIN+3
ENTRYPOINT [ "/sbin/init" ] 
