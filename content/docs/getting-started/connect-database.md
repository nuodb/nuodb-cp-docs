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

Database SQL clients connect through the Ingress controller and require TLS to be enabled on the NuoDB database.

{{< tabs "connect-database" >}}
{{< tab "nuodb-cp" >}}

```sh
nuodb-cp database connect acme/messaging/demo \
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

### Quick links

{{< card-grid >}}
{{< card title="Client Development" icon="outline/book" color="yellow" >}}

- [NuoDB Drivers](https://doc.nuodb.com/nuodb/latest/client-development/nuodb-drivers/)
- [Samples](https://doc.nuodb.com/nuodb/latest/client-development/sample-nuodb-programs-on-github/)

{{< /card >}}
{{< card title="SQL Development" icon="outline/database" color="purple" >}}

- [Using NuoDB SQL CLI](https://doc.nuodb.com/nuodb/latest/sql-development/using-nuodb-sql-command-line/)
- [SQL Statements](https://doc.nuodb.com/nuodb/latest/reference-information/sql-language/sql-statements/)
- [SQL Procedures, Functions, Triggers](https://doc.nuodb.com/nuodb/latest/sql-development/sql-procedures-functions-and-triggers/)

{{< /card >}}
{{< /card-grid >}}
