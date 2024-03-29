# BROKEN: Install Clustering Storage on the Student Application Cluster

Using OpenEBS and cStor. Instructions derived from:

    https://github.com/openebs/cstor-operators/blob/master/docs/quick.md

## Install cStor Chart 

Install the chart:

```
helm repo add openebs https://openebs.github.io/charts
helm repo add openebs-cstor https://openebs.github.io/cstor-operators
helm repo update
```

This command was given to us by the OpenEBS people specific to microk8s:

```
helm install openebs-cstor openebs-cstor/cstor -n openebs --set-string csiNode.kubeletDir="/var/snap/microk8s/common/var/lib/kubelet/" --set openebsNDM.enabled=false
```

## Create a Storage Cluster

The file `supermicro-ssd.yaml` creates a three-way redundant data pool on the Supermicro machines which all have a spare SSD. 

```
kubectl apply -f supermicro-ssd.yaml 
```

Verify (it takes a while):

```
kubectl get cspc -n openebs
```

## Create the Default Storage Class 

This storage class should be the default, it's slower but resilient across all thre SM machines: 

```
kubectl apply -f resilient-storageclass.yaml 
```

## Monitoring 

Assuming that `microk8s enable dashboard` has been run, create a service account binding. This gives dashboard root permissions:

```
kubectl -n kube-system delete clusterrolebinding/kubernetes-dashboard
kubectl apply -f dashboard-rolebinding.yaml
```

Now get the auth token so you can log into the admin site: NOTE: The secret name will change.

```
kubectl get serviceaccounts kubernetes-dashboard -n kube-system -o yaml
kubectl -n kube-system get secret/$(kubectl get serviceaccounts kubernetes-dashboard -n kube-system -o=jsonpath="{.secrets[*].name}") -o yaml
```

Get just the decoded token:

```
kubectl -n kube-system get secret/$(kubectl get serviceaccounts kubernetes-dashboard -n kube-system -o=jsonpath="{.secrets[*].name}") -o 'jsonpath={.data.token}' | base64 -d ; echo ""
```

Make a tunnel to the dashboard: 

```
kubectl -n kube-system port-forward svc/kubernetes-dashboard 8080:443
```

## EFK (WIP)

This cluster badly needs monitoring. This work in progress will enable the EFK stack so that I can consolidate logging and monitoiring. There is a microk8s addon: 

https://microk8s.io/docs/addon-fluentd

Enable the add-on:

```
microk8s enable fluentd
```

Access the dashboard: 

```
kubectl port-forward -n kube-system service/kibana-logging 8080:5601
```
