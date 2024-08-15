---
title: "Create your first Database"
description: ""
summary: ""
date: 2024-08-14T13:37:13+03:00
lastmod: 2024-08-14T13:37:13+03:00
draft: false
weight: 130
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

Once the Control Plane is deployed, projects and databases can now be created.

## Prerequisites

- [nuodb-cp][1] or [cURL](https://curl.se/download.html)
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
alias curl="curl -s -k -i -u \"${NUODB_CP_USER}:${NUODB_CP_PASSWORD}\""
```

## Create Project

Create a new project *messaging* in organization *acme*:

{{< tabs "create-new-project" >}}
{{< tab "nuodb-cp" >}}

```sh
nuodb-cp project create acme/messaging \
  --sla "dev" \
  --tier n0.small
```

{{< /tab >}}
{{< tab "curl" >}}

```sh
curl -X PUT -H 'Content-Type: application/json' \
    $NUODB_CP_URL_BASE/projects/acme/messaging \
    -d '{"sla": "dev", "tier": "n0.small"}'
```

{{< /tab >}}
{{< /tabs >}}

{{< callout context="note" title="Note" icon="outline/info-circle" >}}
Creating project and database with `n0.small` service tier will require 3 vCPU and 5Gi RAM allocatable resources from your cluster.
If your setup is resource constrained, consider using `n0.nano` service tier.
{{< /callout >}}

## Create database

Create a new database *demo* in project *messaging*:

{{< tabs "create-new-database" >}}
{{< tab "nuodb-cp" >}}

```sh
nuodb-cp database create acme/messaging/demo \
  --dba-password changeIt
```

{{< /tab >}}
{{< tab "curl" >}}

```sh
curl -X PUT -H 'Content-Type: application/json' \
    $NUODB_CP_URL_BASE/databases/acme/messaging/demo \
    -d '{"dbaPassword": "changeIt"}'
```

{{< /tab >}}
{{< /tabs >}}

Wait for the database to become available.

{{< tabs "wait-new-database" >}}
{{< tab "nuodb-cp" >}}

```sh
while [ "$(nuodb-cp database get acme/messaging/demo | jq -r '.status.ready')" != "true" ]; do
  echo "Waiting ..."
  sleep 5
done
echo "Database is available"
```

{{< /tab >}}
{{< tab "curl" >}}

```sh
while [ "$(curl $NUODB_CP_URL_BASE/databases/acme/messaging/demo | jq '.status.ready')" != "true" ]; do
  echo "Waiting ..."
  sleep 5
done
echo "Database is available"
```

{{< /tab >}}
{{< /tabs >}}

[1]: https://github.com/nuodb/nuodb-cp-releases/releases/latest/download/nuodb-cp
