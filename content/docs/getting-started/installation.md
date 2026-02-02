---
title: "Deploy NuoDB Control Plane"
description: ""
summary: ""
date: 2024-08-14T13:27:07+03:00
lastmod: 2024-08-14T13:27:07+03:00
draft: false
weight: 110
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

NuoDB Control Plane allows users to provision NuoDB databases on-demand remotely using REST services by exposing various predefined configuration options.

This page describes how to deploy the NuoDB Control Plane into your Kubernetes Cluster.
The NuoDB Control Plane works with [Kubernetes][1] locally or in the cloud.
Follow the steps in this guide regardless of the selected Kubernetes platform provider.

## Prerequisites

- A running [Kubernetes cluster][2]
- [kubectl][3] installed and able to access the cluster.
- [Helm 3.x][4] installed.

## Software Dependency Installation

### Install Cert Manager

To enable [admission webhooks][7] in the NuoDB operator, install [cert-manager](https://github.com/cert-manager/cert-manager) to automatically generate certificates for the webhook server.

Add the official Helm repositories.

```sh
helm repo add jetstack https://charts.jetstack.io
helm repo update
```

Install Cert Manager Helm chart.

```sh
helm upgrade --install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --wait \
  --set installCRDs=true
```

### Install Ingress Controller

NuoDB databases support [external access](https://github.com/nuodb/nuodb-helm-charts/blob/master/docs/HowToConnectExternally.md) from clients that are outside of Kubernetes cluster.
The NuoDB Control Plane (CP) can be configured to allow external connections to the REST service to create domains and databases.
It configures databases with external access also, providing connection details for each database.

NuoDB CP supports [Ingress Nginx](https://kubernetes.github.io/ingress-nginx) and [HAProxy](https://github.com/haproxytech/kubernetes-ingress) ingress controllers.
The SSL-passthrough feature is used to expose and multiplex SQL database connectivity.

Add the official Ingress Nginx Helm repositories.

```sh
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
```

Install Ingress Nginx Controller.

```sh
helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace nginx \
  --create-namespace \
  --set controller.ingressClassResource.default=true \
  --set controller.service.enablePorts.http=false \
  --set controller.admissionWebhooks.certManager.enabled=true \
  --set controller.extraArgs.default-ssl-certificate="nginx/ingress-nginx-default-cert" \
  --set controller.extraArgs.enable-ssl-passthrough=true \
  --set controller.service.type=NodePort # Enables connecting to databases with port-forwarding
```

Generate TLS certificates for Ingress Controller.

```sh
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: ingress-nginx-default-cert
  namespace: nginx
spec:
  commonName: dbaas.localtest.me
  duration: 8760h
  issuerRef:
    name: ingress-nginx-self-signed-issuer
  secretName: ingress-nginx-default-cert
  subject:
    organizations:
    - ingress-nginx
EOF
```

{{< callout context="caution" title="Caution" icon="outline/alert-triangle" >}}
Self-signed certificates should be used for local testing purposes only.
For more information on how to configure Nginx controller with TLS, see [Ingress Nginx TLS User Guide](https://github.com/kubernetes/ingress-nginx/blob/main/docs/user-guide/tls.md).
{{< /callout >}}

## Obtain NuoDB license

The installation of either a Limited Use License or an Enterprise License is required to create and start NuoDB databases.
For more information on NuoDB licenses, see [NuoDB Product Licenses](https://doc.nuodb.com/nuodb/latest/introduction-to-nuodb/#_nuodb_product_licenses).
To obtain the license file required to enable deployment of the Limited Use License or the Enterprise License, contact [NuoDB Support](mailto:NuoDB.Support@3ds.com).

The contents of NuoDB license files have following form:

```text
-----BEGIN LICENSE-----
<base64-encoded data>
-----END LICENSE-----
```

{{< callout context="note" title="Note" icon="outline/info-circle" >}}
Set the path to the NuoDB license file using `export LICENSE_FILE=</path/to/nuodb.lic>`.
The environment variable is used in the NuoDB Control Plane installation commands.
{{< /callout >}}

## Installing NuoDB Control Plane

The NuoDB Control Plane consists of [Custom Resource Definitions][5] and the following workloads:

- The *NuoDB CP Operator*, which enforces the desired state of the NuoDB [custom resources][6].
- The *NuoDB CP REST service*, that exposes a REST API allowing users to manipulate and inspect DBaaS entities.

Databases are grouped into *projects*, which are themselves grouped into *organizations*.

{{< callout context="note" title="Note" icon="outline/info-circle" >}}
By default the NuoDB CP will operate in a single namespace only which will be used for NuoDB CP and all databases created by it.
{{< /callout >}}

Add the official Helm repositories.

```sh
helm repo add nuodb-cp https://nuodb.github.io/nuodb-cp-releases/charts
helm repo update
```

Install NuoDB CP Helm charts.

```sh {title="Install DBaaS CRDs"}
helm upgrade --install nuodb-cp-crd nuodb-cp/nuodb-cp-crd \
    --namespace nuodb-cp-system \
    --create-namespace
```

```sh {title="Install DBaaS operator"}
helm upgrade --install nuodb-cp-operator nuodb-cp/nuodb-cp-operator \
    --namespace nuodb-cp-system \
    --wait \
    --set cpOperator.webhooks.enabled=true \
    --set nuodb-cp-config.nuodb.license.enabled=true \
    --set nuodb-cp-config.nuodb.license.secret.create=true \
    --set nuodb-cp-config.nuodb.license.secret.name=nuodb-license \
    --set nuodb-cp-config.nuodb.license.content="$(cat ${LICENSE_FILE})" \
    --set 'cpOperator.extraArgs[0]=--ingress-https-port=8443' # Enables connecting to databases with port-forwarding
```

```sh {title="Install DBaaS REST service"}
helm upgrade --install nuodb-cp-rest nuodb-cp/nuodb-cp-rest \
    --namespace nuodb-cp-system \
    --wait \
    --set cpRest.ingress.enabled=true \
    --set "cpRest.baseDomainName=dbaas.localtest.me" # Enables connecting to databases with port-forwarding
```

[1]: https://kubernetes.io/docs/home/
[2]: https://kubernetes.io/docs/concepts/overview/components/
[3]: https://kubernetes.io/docs/tasks/tools/
[4]: https://helm.sh/
[5]: https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#customresourcedefinitions
[6]: https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#custom-resources
[7]: https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/
