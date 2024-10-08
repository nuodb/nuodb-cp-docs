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

Once the Control Plane is deployed, projects and databases can be created.

{{< callout context="tip" title="Check out" icon="outline/rocket" >}}
For more information on the available services, see [REST API reference]({{< ref "../reference/rest-api.md" >}}).
{{< /callout >}}

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
{{< tab "terraform" >}}

```terraform
resource "nuodbaas_project" "proj" {
  organization = "acme"
  name         = "messaging"
  sla          = "dev"
  tier         = "n0.small"
}
```

{{< /tab >}}
{{< /tabs >}}

{{< callout context="note" title="Note" icon="outline/info-circle" >}}
Creating project and database with `n0.small` service tier requires 3 vCPUs and 5Gi of RAM.
If your environment is resource constrained, consider using the `n0.nano` service tier.
{{< /callout >}}

## Create database

Create a new database *demo* in the *messaging* project.

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
{{< tab "terraform" >}}

```terraform
resource "nuodbaas_database" "db" {
  organization = nuodbaas_project.proj.organization
  project      = nuodbaas_project.proj.name
  name         = "demo"
  dba_password = "changeIt"
}
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
{{< tab "terraform" >}}

Terraform waits until all resources are available before reporting a success.

{{< /tab >}}
{{< /tabs >}}
