---
title: "DatabaseUnavailable"
description: ""
summary: ""
date: 2025-06-05T13:52:09+03:00
lastmod: 2025-06-05T13:52:09+03:00
draft: false
weight: 103
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

## Meaning

Database is not available.

{{< details "Full context" open >}}
Database is not available to SQL applications.
There are no Transaction Engines (TEs) ready to service clients.
{{< /details >}}

## Impact

Service unavailability.

The database is down and SQL applications can't connect.

## Diagnosis

See [Diagnosing database component]({{< ref "databasecomponentunreadyreplicas#diagnosis" >}}).

### Scenarios

See [Database component failures]({{< ref "databasecomponentunreadyreplicas#scenarios" >}}).
