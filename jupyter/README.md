# Setup Zero to Jupyterhub 

## Setup

There must be a default storage class available.

## Helm Setup 

Jupyterhub handles Let's Encrypt certificates internally. 

```
helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
helm repo update
```

Install JupyterHub:

```
helm install -n jhub --create-namespace jhub jupyterhub/jupyterhub --values values.yaml --values secrets.yaml
```

Update JupyterHub:

```
helm upgrade -n jhub jhub jupyterhub/jupyterhub --values values.yaml --values secrets.yaml
```

