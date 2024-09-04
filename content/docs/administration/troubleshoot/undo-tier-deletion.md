---
title: "Undo Tier Configuration Deletion"
description: ""
summary: ""
date: 2024-08-14T13:52:09+03:00
lastmod: 2024-08-14T13:52:09+03:00
draft: false
weight: 905
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

This guide describes how to re-create deleted NuoDB Control Plane(CP) service tier configuration.

## Service Tier and Helm Feature Deletion

The NuoDB CP creates and uses kubernetes custom resource definitions(CRDs) to describe and set different service tiers and NuoDB helm chart values for domain and database resources. The NuoDB operator sets [Finalizers](https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/) on these resources to prevent deletion of a tier or feature while they are actively used by running domains and databases.

If a service tier or a helm feature is unintentionally deleted, by automation or human error, it will leave the resource in a deleted state, for example:

```json
{
  "level":"error",
  "ts":"2023-02-10T16:55:10.098Z",
  "logger":"controller.servicetier",
  "msg":"unable to delete service tier",
  "reconciler group":"cp.nuodb.com",
  "reconciler kind":"ServiceTier",
  "name":"n0.small",
  "namespace":"nuodb-cp-system",
  "error":"resources that have reference to service tier nuodb-cp-system/n0.small: [domain/nuodb-cp-system/acme-messaging database/nuodb-cp-system/acme-messaging-demo]"
}
```

While domain and database objects continue to operate as normal, future updates will not be possible until the deletion is reversed.

### Service Tier

To reverse the deletion of a service tier, first list all service tiers that are in a deleted state:

```sh
kubectl get tier -o jsonpath='{.items[?(@.metadata.deletionTimestamp)].metadata.name}'
```

This will return an output similar to:

```text
n0.small
...
```

A change in a service tier is directly propagated to all databases.
Both the domain and the database controllers will perform validation of the resource before the actual reconciliation.

{{< callout context="note" title="Note" icon="outline/info-circle" >}}
Once a tier resource is force deleted (by manually removing its finalizers), all domains and databases that reference it will transition its `Ready` condition to False with reason `ValidationFailed`.
{{< /callout >}}

After the tier resource is re-created, the databases will be reported ready almost instantly.
No database Pod restarts will be performed and the service won't be interrupted during this time.

Export the selected service tier as YAML:

```sh
kubectl get tier n0.small -o yaml | sed -e '/deletionTimestamp/d' -e '/deletionGracePeriodSeconds/d'  > tier-backup.yaml
```

Re-create the service tier:

```sh
kubectl patch tier n0.small -p '{"metadata":{"finalizers":null}}' --type=merge
kubectl create -f tier-backup.yaml
```

### Helm Feature

To reverse the deletion of a helm feature, first list all helm features that are in a deleted state:

```sh
kubectl get feature -o jsonpath='{.items[?(@.metadata.deletionTimestamp)].metadata.name}'
```

This will return an output similar to:

```text
small-resources
...

```

There is a level of indirection as the features are referenced in tiers.
A database reconciliation will be triggered only if the `cp.nuodb.com/features-hash` annotation value changes.
If a referenced feature is force removed (by manually removing it's finalizers), the hash calculation will fail, preventing event propagation to all databases.

Example error for hash calculation:

```json
{
  "level":"error",
  "ts":"2023-03-06T08:43:44.846Z",
  "msg":"unable to find referenced features",
  "controller":"servicetier",
  "controllerGroup":"cp.nuodb.com",
  "controllerKind":"ServiceTier",
  "ServiceTier":{
    "name":"n1.small",
    "namespace":"nuodb-cp-system"
  },
  "namespace":"nuodb-cp-system",
  "name":"n1.small",
  "reconcileID":"5d6350be-e9c9-450a-b5cc-67b92816378f",
  "error":"HelmFeature.cp.nuodb.com \"small-resources\" not found",
  "errorCauses":[{"error":"HelmFeature.cp.nuodb.com \"small-resources\" not found"}]}
```

Export the selected service tier as YAML:

```sh
kubectl get feature small-resources -o yaml | sed -e '/deletionTimestamp/d' -e '/deletionGracePeriodSeconds/d'  > feature-backup.yaml
```

Re-create the service tier:

```sh
kubectl patch feature small-resources -p '{"metadata":{"finalizers":null}}' --type=merge
kubectl create -f feature-backup.yaml
```
