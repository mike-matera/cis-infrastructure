# Setup Zero to Jupyterhub 

## Setup

I changed the local path to the host provisioner and set a default storage class: 

```
kubectl apply -f local-ssd-storageclass.yaml
```

## Helm Setup 

Jupyterhub handles Let's Encrypt certificates internally. 

```
helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
helm repo update
```

Install JupyterHub:

```
helm install jhub jupyterhub/jupyterhub --values values.yaml --values secrets.yaml
```

Update JupyterHub:

```
helm upgrade jhub jupyterhub/jupyterhub --values values.yaml --values secrets.yaml
```

