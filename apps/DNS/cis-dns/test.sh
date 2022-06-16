#! /bin/sh 

set -e 

if [ -z "$DNS_ROLE" ]; then
    echo "ERROR!"
    echo "You must specify a value fro \$DNS_ROLE, either internal or external"
    exit -1 
fi 

python3 ./gen-db.py
cp build/db.* /etc/bind/
chown -R bind:bind /etc/bind

cp named-$DNS_ROLE.conf /etc/bind/named-$DNS_ROLE.conf 
/usr/sbin/named -g -c /etc/bind/named-$DNS_ROLE.conf -u bind &
sleep 2
exec python3 ./test.py 

