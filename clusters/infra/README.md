# Setup the Infrastructure Cluster 

This is the Cliff's notes. 

## Apply the Playbook 

```console
$ ansible-playbook -i inventory.yaml playbook.yaml
```

This creates `kube-config-*` files. Do not check them in. Install them. 

