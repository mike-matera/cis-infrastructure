# Setup Zero to Jupyterhub 

## Setup

I changed the local path to the host provisioner and set a default storage class: 

```
kubectl apply -f local-ssd-storageclass.yaml
```

Create a service for the load balancer so it gets an IP address: 

```
kubectl apply -f ingress-service.yaml
```

## Install Cert Manager 

```
kubectl create namespace cert-manager
helm repo add jetstack https://charts.jetstack.io
helm repo update
helm install \
  cert-manager jetstack/cert-manager \
  --version v1.4.0 \
  --namespace cert-manager \
  --create-namespace \
  --set installCRDs=true
```

Apply the issuer config:

```
kubectl apply -n cert-manager -f ./issuer-selfsigned.yaml 
kubectl apply -n cert-manager -f ./issuer-letsencrypt.yaml 
```


## Helm Setup 

```
helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
helm repo update
```

Install JupyterHub:

```
helm install jhub jupyterhub/jupyterhub --values values.yaml
```

