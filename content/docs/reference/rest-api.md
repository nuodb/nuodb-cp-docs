---
title: "REST API Reference"
description: "NuoDB Control Plane REST Service API reference"
summary: ""
date: 2023-09-07T16:13:18+02:00
lastmod: 2023-09-07T16:13:18+02:00
draft: false
weight: 910
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

The NuoDB Control Plane REST API exposes access to resources in a hierarchical structure.

- An _organization_ contains several _projects_ and _users_.
- A _user_ is an entity that authenticates itself and issues requests to resources that it has been granted access to.
- A _project_ contains several _databases_ and enables both logical and physical separation between databases.
Databases belonging to the same project share resources associated with the project (i.e. a NuoDB domain), while databases in different projects do not share these resources and are more isolated from each other.

## Further reading

- [REST API reference](https://nuodb.github.io/nuodb-cp-releases/api-doc/)
