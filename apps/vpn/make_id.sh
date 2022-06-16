#! /bin/bash 

if [ -z "$1" -o -z "$2" ]; then 
    echo "ussge: $0 <ipaddr> <output>"
    exit -1 
fi 

set -e 

ipaddr=$1
priv="${2}_private.key"
pub="${2}_public.key"
conf="${2}.conf"

priv_key=$(wg genkey | tee $priv)
pub_key=$(wg pubkey < $priv | tee $pub)

cat > $conf <<EOF
[Interface]
Address = ${ipaddr}/24
PrivateKey = ${priv_key}

[Peer]
PublicKey = hwjtU8u9CudQ5K7qmkwDTQcmnyMOxzTqz/rmPzcKJVk=
AllowedIPs = 10.8.0.0/24, 172.30.5.0/24, 192.168.0.0/24
Endpoint = vpn.cis.cabrillo.edu:51820
EOF

cat <<EOF
Local definition: 

[Peer]
PublicKey = ${pub_key}
AllowedIPs = ${ipaddr}/32
EOF
