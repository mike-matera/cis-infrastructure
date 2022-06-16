# DNS Hosting in Kubernetes 

FIXME: More 

## Loading the DNS configuration

Load the config map from the file in hosts: 

```
kubectl -n cis-dns create configmap cis-dns --from-file=hosts/10-inventory.yaml
```

## Updating the DNS configuration 

First update the configmap:

```console
kubectl create configmap cis-dns --from-file=hosts/10-inventory.yaml -o yaml --dry-run=client | kubectl -n cis-dns apply -f  - 
```

Then roll the deployment: 

```console
kubectl -n cis-dns rollout restart deployment cis-dns-external cis-dns-internal 
```
