---
title: "DomainUnavailable"
description: ""
summary: ""
date: 2025-06-05T13:52:09+03:00
lastmod: 2025-06-05T13:52:09+03:00
draft: false
weight: 107
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

## Meaning

Domain is not available.

{{< details "Full context" open >}}
Domain is not available to load-balance SQL clients or accept database configuration changes.
There are no NuoDB Admin processes (APs) ready in the NuoDB domain.
{{< /details >}}

## Impact

Service unavailability.

New SQL connections to any database in the domain will fail.
Already established SQL connections are not impacted.
No new database processes can be started in this domain.

## Diagnosis

See [Diagnosing domain component]({{< ref "domaincomponentunreadyreplicas#diagnosis" >}}).

### Scenarios

See [Domain component failures]({{< ref "domaincomponentunreadyreplicas#scenarios" >}}).
