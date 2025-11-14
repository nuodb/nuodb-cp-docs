---
title: "User Access Control Rules"
description: ""
summary: ""
date: 2024-08-14T13:52:09+03:00
lastmod: 2024-08-14T13:52:09+03:00
draft: false
weight: 215
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---


Access Rule Entries define what permissions a user has to one or multiple resources.
These permissions are defined during a [user create/update]({{< ref "user-management.md" >}}#creating-users) operation or optionally when creating an [authentication token]({{< ref "token-authentication.md" >}}) for a user.

An access rule entry has the format `<verb>:<resource specifier>[:<SLA>]`.

### Verb

A _verb_ is one of the following and is associated with one or more HTTP methods.

| verb     | HTTP methods                    |
| -------- | ------------------------------- |
| `read`   | `GET`                           |
| `write`  | `PUT`, `PATCH`                  |
| `delete` | `DELETE`                        |
| `all`    | `GET`, `PUT`, `PATCH`, `DELETE` |

### Resource specifier

A _resource specifier_ takes one of two forms:

- If a resource specifier starts with `/`, then it is interpreted as an absolute resource path.
  The first component of the path must be a resource type, such as `/projects`, `/databases/`, `/users`, and `/healthz`.
- Otherwise, it is interpreted as a _scope_, which has the format `<organization>/<project>/<database>`, `<organization>/<project>`, or `<organization>`.
  A scope binds to a specific object in the hierarchy of DBaaS objects (_organizations_, _projects_, _databases_) and expands to the set of resource paths associated with that object.
  For example, the scope `acme` expands to the resource paths `/projects/acme/*`, `/databases/acme/*`, and `/users/acme/*`, while `acme/messaging` expands to `/projects/acme/messaging/*` and `/databases/acme/messaging/*`.

### SLA

An optional third component of the access rule entry limits access to only projects that have matching SLA values and databases within those projects.
For example, `write:acme:dev` would grant write access to all projects within the `acme` organization with SLA `dev` and all of their databases.

Only `allow` entries accept an SLA value.

### Example: Full access

To grant full access to all resources, the wildcard resource can be specified.

```json
{
  "allow": "all:*"
}
```

{{< callout context="note" title="Note" icon="outline/info-circle" >}}
Either (or both) of the `allow` and `deny` fields in the access rule can be omitted or supplied with a string value, which expands to a single element array.
{{< /callout >}}

### Example: Read and write access at different levels

To grant read access at the organization level and write access at the project level, the following can be specified.

```json
{
  "allow": ["read:acme", "write:acme/messaging"]
}
```

The rule above allows projects, databases, and users to be listed for the organization `acme` and allows the specific project `acme/messaging` to be written, as well as any database within `acme/messaging`.

### Example: Access to specific resource paths

Access can be granted to specific resource paths as follows:

```json
{
  "allow": ["all:acme/messaging/demo", "all:/users/acme/dbuser"]
}
```

In the example above, the resource `/users/acme/dbuser` is specified to grant full access to that specific user.
This would allow a user to change its own password without having access to all resources at the organization level.

### Example: Denying access to resource paths

Access to specific resource paths can also be explicitly denied using the `deny` field.

```json
{
  "allow": "all:acme",
  "deny": "all:/users/*"
}
```

In the example above, full access is granted for all resources in the `acme` organization, except users.
Note that this is equivalent to the following access rule, assuming that the set of root resources expanded by an organization scope is `/projects`, `/databases`, and `/users`:

```json
{
  "allow": ["all:/projects/acme/*", "all:/databases/acme/*"]
}
```

Although the two access rules are equivalent for the current version of the Control Plane REST API, they would behave differently if changes are made to the API.
The former would grant access to any organization-scoped resources that are added to the API, while the latter would not.
It is up to the administrator to decide which approach is best.

### Example: Access to multiple organizations

Even though each user belongs to a specific organization, it is possible to grant users access to multiple organizations, as shown below:

```json
{
  "allow": ["all:acme", "read:notacme"]
}
```

{{< callout context="note" title="Note" icon="outline/info-circle" >}}
Adding access outside of a user's organization requires specifying the query parameter `allowCrossOrganizationAccess=true`, which is accepted by both `PUT` and `PATCH` requests on the user resource.
{{< /callout >}}

### Example: Access constrained by SLA

To grant access to only the projects and databases within a scope that have a particular SLA value, an SLA constraint can be specified:

```json
{
  "allow": ["all:acme:dev", "read:acme:qa", "write:acme/messaging"]
}
```

In the example above, full access is granted to all projects and databases in `acme` that have SLA `dev`, read access is granted to projects and databases in `acme` that have SLA `qa`, and write access is granted to the specific project `acme/messaging`.
