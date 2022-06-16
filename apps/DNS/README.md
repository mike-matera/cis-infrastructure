# DNS Hosting in Kubernetes 

FIXME: More 

## Loading the DNS configuration

Load the config map from the file in hosts: 

```
kubectl -n cis-dns create configmap cis-dns --from-file=hosts/10-inventory.yaml
```