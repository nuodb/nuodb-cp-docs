---
title: "Connect to NuoDB Control Plane"
description: ""
summary: ""
date: 2024-08-14T13:37:13+03:00
lastmod: 2024-08-14T13:37:13+03:00
draft: false
weight: 120
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

This section describes how to connect to NuoDB Control Plane REST service via CLI tools.

{{< callout context="tip" title="Check out" icon="outline/rocket" >}}
For more information on the available services, see [REST API reference](docs/reference/rest-api-reference/).
{{< /callout >}}

## Prerequisites

- [nuodb-cp](https://github.com/nuodb/nuodb-cp-releases/releases/latest/download/nuodb-cp) or [cURL](https://curl.se/download.html)
- [jq](https://jqlang.github.io/jq/download/)

## Access and Authentication

This guide uses port forwarding to access the REST API and provisioned databases.

```sh
kubectl port-forward svc/ingress-nginx-controller -n nginx 8443:443 2>&1 >/dev/null &
```

### Download NuoDB Control Plain CLI tool

```sh
curl -sL https://github.com/nuodb/nuodb-cp-releases/releases/latest/download/nuodb-cp -o /usr/local/bin/nuodb-cp
chmod a+x /usr/local/bin/nuodb-cp
```

### Setup DBaaS credentials

To successfully authenticate with the REST API, configure the credentials as environment variables.

```sh
export NUODB_CP_URL_BASE="https://localhost:8443/nuodb-cp"
export NUODB_CP_USER="system/admin"
export NUODB_CP_PASSWORD="$(kubectl get secret dbaas-user-system-admin -n nuodb-cp-system -o jsonpath='{.data.password}' | base64 -d)"
```

{{< callout context="note" title="Note" icon="outline/info-circle" >}}
The *system/admin* is the first cluster administrator user created during installation.
It is recommended to create less privileged users after installation.
For more information, see [User Management and Access Control](/docs/administration/user-management-and-access-control).
{{< /callout >}}

If Nginx TLS certificate in not signed by public CA, `nuodb-cp` must configured to trust it.

```sh
kubectl get secret ingress-nginx-default-cert -n nginx -o jsonpath='{.data.ca\.crt}' | base64 -d > /tmp/ingress.pem
export NUODB_CP_TRUSTED_CERT=/tmp/ingress.pem
```

Configure `cURL` with DBaaS credentials.

```sh
alias curl="curl -s -k -u \"${NUODB_CP_USER}:${NUODB_CP_PASSWORD}\""
```
