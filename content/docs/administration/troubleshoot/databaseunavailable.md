---
title: "DatabaseUnavailable"
description: ""
summary: ""
date: 2025-06-05T13:52:09+03:00
lastmod: 2025-06-05T13:52:09+03:00
draft: false
weight: 480
toc: true
seo:
  title: "" # custom title (optional)
  description: "Database is not available to SQL applications" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

## Meaning

Database is not available.

{{< details "Full context" open >}}
Database is not available to SQL applications.
There are no Transaction Engines (TEs) ready to service clients.
{{< /details >}}

### Symptom

To manually evaluate the conditions for this alert, see [Unready database component symptom]({{< ref "databasecomponentunreadyreplicas#symptom" >}}).

## Impact

Service unavailability.

The database is down and SQL applications can't connect.

## Diagnosis

See [Diagnosing database component]({{< ref "databasecomponentunreadyreplicas#diagnosis" >}}).

### Scenarios

See [Database component failures]({{< ref "databasecomponentunreadyreplicas#scenarios" >}}).
