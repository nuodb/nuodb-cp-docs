---
title: "RoleTemplate"
description: "A sample RoleTemplate object with fields documented"
summary: ""
draft: false
weight: 963
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

## Minimal example

```yaml
# Standard Kubernetes API Version declaration.
apiVersion: cp.nuodb.com/v1beta1
# Standard Kubernetes Kind declaration.
kind: RoleTemplate
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-roletemplate
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the RoleTemplate.
spec:
  # List of access rule entries to allow.
  allow:
  -
    # The resource or set of resources to grant access to. If the value
    # begins with a slash (`/`), then the value denotes a resource path.
    # Otherwise, the value denotes a scope in the hierarchy of the DBaaS
    # resources that this access rule entry grants access to, of the form
    # `<organization>`, `<organization>/<project>`, or
    # `<organization>/<project>/<database>`. In either case, parameterized
    # path segments of the form `{organization}` or `{user}` may appear
    # that are resolved when the role template is assigned to a user.
    resource: string
    # The verb to grant access to with this access rule entry, which maps
    # to HTTP request methods as follows:
    # 
    # - `read`: GET
    # - `write`: PUT, POST
    # - `delete`: DELETE
    # 
    # `all` denotes that the request method is unconstrained for this
    # access rule entry.
    verb: read
```

## Extended example

```yaml
# Standard Kubernetes API Version declaration.
apiVersion: cp.nuodb.com/v1beta1
# Standard Kubernetes Kind declaration.
kind: RoleTemplate
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-roletemplate
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the RoleTemplate.
spec:
  # List of access rule entries to allow.
  allow:
  -
    # The resource or set of resources to grant access to. If the value
    # begins with a slash (`/`), then the value denotes a resource path.
    # Otherwise, the value denotes a scope in the hierarchy of the DBaaS
    # resources that this access rule entry grants access to, of the form
    # `<organization>`, `<organization>/<project>`, or
    # `<organization>/<project>/<database>`. In either case, parameterized
    # path segments of the form `{organization}` or `{user}` may appear
    # that are resolved when the role template is assigned to a user.
    resource: string
    # The SLA to constrain access to. This constraint only applies to
    # projects and resources contained within projects, such as databases
    # and backups.
    sla: prod
    # The verb to grant access to with this access rule entry, which maps
    # to HTTP request methods as follows:
    # 
    # - `read`: GET
    # - `write`: PUT, POST
    # - `delete`: DELETE
    # 
    # `all` denotes that the request method is unconstrained for this
    # access rule entry.
    verb: read
# Current observed status of the RoleTemplate.
status:
```
