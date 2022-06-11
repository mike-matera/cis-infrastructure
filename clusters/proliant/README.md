# Setup the New Proliant Cluster 

This is the Cliff's notes. 

## Apply the Playbook 

```console
$ ansible-playbook -i inventory.yaml playbook.yaml
```

This creates `kube-config-*` files. Do not check them in. Install them. 

## Setup Kubernetes 

Create the Mayastor pools for the SSDs:

```console
$ kubectl apply -f mayastor-ssd-pools.yaml
```

Verify they are healthy (this might take a bit):

```console
$ kubectl get -n mayastor msp
NAME             NODE         STATUS   CAPACITY       USED   AVAILABLE
proliant-3-sdb   proliant-3   Online   999225819136   0      999225819136
proliant-2-sdb   proliant-2   Online   999225819136   0      999225819136
proliant-1-sdb   proliant-1   Online   999225819136   0      999225819136
proliant-4-sdb   proliant-4   Online   999225819136   0      999225819136
```

Create the Mayastor storage classes (including the default) and remove the default ones:

```console
$ kubectl apply -f mayastor-storage-class.yaml
$ kubectl delete sc mayastor mayastor-3
```

Verify them: 

```console
$ kubectl get sc
NAME               PROVISIONER               RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
ssd-ha (default)   io.openebs.csi-mayastor   Delete          WaitForFirstConsumer   false                  2m20s
ssd                io.openebs.csi-mayastor   Delete          WaitForFirstConsumer   false                  2m20s
```

Create the cStore pool with the HDDs:

```console 
$ kubectl apply -f cstor-disk-pools.yaml
```

Wait for the containers to start running and create the HDD storage classes. 

```console 
$ kubectl apply -f cstor-storage-class.yaml
```
