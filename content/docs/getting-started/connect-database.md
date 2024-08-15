---
title: "Connect to the Database"
description: ""
summary: ""
date: 2024-08-14T13:40:00+03:00
lastmod: 2024-08-14T13:40:00+03:00
draft: false
weight: 140
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

Database SQL connections are going through the Ingress controller and requires TLS to be enabled on NuoDB database.

{{< tabs "connect-database" >}}
{{< tab "nuodb-cp" >}}

```sh
nuodb-cp database connect acme/messaging/demo \
  --ingress-port 8443 \
  --db-user=dba \
  --db-password=changeIt
```

{{< /tab >}}
{{< tab "nuosql" >}}

Get database connection information.

```sh
CA_CERT="$(curl $NUODB_CP_URL_BASE/databases/acme/messaging/demo | jq -r '.status.caPem')"
DB_URL="$(curl $NUODB_CP_URL_BASE/databases/acme/messaging/demo | jq -r '.status.sqlEndpoint')"
```

Connect using `nuosql`.

```sh
nuosql "demo@${DB_URL}:8443" --user dba --password changeIt --connection-property trustedCertificates="$CA_CERT"
```

[NuoDB client](https://github.com/nuodb/nuodb-client/releases) package v20230228 or later is required to connect to DBaaS database.

{{< /tab >}}
{{< /tabs >}}


