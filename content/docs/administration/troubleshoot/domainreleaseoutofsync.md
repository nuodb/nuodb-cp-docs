---
title: "DomainReleaseOutOfSync"
description: ""
summary: ""
date: 2025-06-05T13:52:09+03:00
lastmod: 2025-06-05T13:52:09+03:00
draft: false
weight: 471
toc: true
seo:
  title: "" # custom title (optional)
  description: "Domain resource desired state is out of sync" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

## Meaning

Domain release is out of sync.

{{< details "Full context" open >}}
Domain resource desired state is out of sync.
The coresponding domain Helm release install/upgrade operation failed to apply the latest Helm values.
{{< /details >}}

### Symptom

To manually evaluate the conditions for this alert follow the steps below.

A domain, in which the desired state is out of sync, will have the `Released` status condition set to `False`.
List all out of sync domains.

```sh
JSONPATH='{range .items[*]}{@.metadata.name}:{range @.status.conditions[?(@.type=="Released")]}{@.type}={@.status}{"\n"}{end}{end}'
kubectl get domain -o jsonpath="$JSONPATH" | grep "Released=False"
```

Inspect the domain `Released` condition message for more details.

```sh
kubectl get domain <name> -o jsonpath='{.status.conditions[?(@.type=="Released")]}' | jq
```

## Impact

Latest domain configuration is not enforced.

New domain won't become available.
Connectivity to already provisioned domains is not impacted by this issue, however, some features that require applying domain configuration changes might be unavailable (e.g. start/stop domain, TLS rotation, etc.).

## Diagnosis

- Check the domain state using `kubectl describe domain <name>`.
- Check the domain `Released` condition's state and message.
- Check the `Released` condition's state and message for the corresponding _HelmApp_ resource.
- List the Helm revisions for the Helm release associated with the domain.
- Check the latest Helm values for the failed Helm release.
- Check that Helm chart repository services are available.
By default, the public NuoDB Helm charts [repository](https://nuodb.github.io/nuodb-helm-charts) in GitHub is used, however, this can be overridden.

### Scenarios

See [Helm operation failures]({{< ref "databasereleaseoutofsync#scenarios" >}}).

### Example

Get the domain name and its namespace from the alert's labels.
Inspect the domain state in the Kubernetes cluster.

```sh
kubectl get domain acme-messaging -n nuodb-cp-system
```

Notice that the `SYNCED` value is `False` which means that the database desired state is not enforced.

```text
NAME                  TIER       VERSION   READY   SYNCED   DISABLED   AGE
acme-messaging        n0.small   6.0.2     False   False    False      62h
```

Inspect the domain `Released` condition.

```sh
kubectl get domain acme-messaging -o jsonpath='{.status.conditions[?(@.type=="Released")]}' | jq
```

The output below indicates issues with the corresponding _HelmApp_ resource `acme-messaging-demo-zfb77wc`.

```json
{
  "lastTransitionTime": "2025-06-10T10:27:21Z",
  "message": "synchronization failed for applications [acme-messaging-fc4bwd8]",
  "observedGeneration": 1,
  "reason": "ReconciliationFailed",
  "status": "False",
  "type": "Released"
}
```

Inspect the _HelmApp_ resource associalted with the domain.

```sh
RELEASE_NAME=$(kubectl get domain acme-messaging -o jsonpath='{.spec.template.releaseName}')
kubectl describe helmapp $RELEASE_NAME
```

Check the `Released` status condition of the _HelmApp_.

```sh
kubectl get helmapp $RELEASE_NAME -o jsonpath='{.status.conditions[?(@.type=="Released")]}' | jq
```

The output below indicates issues Helm upgrade operation.
An existing _ResourseQuota_ limits creation of ConfigMap resources.

```json
{
  "lastTransitionTime": "2025-06-10T10:27:21Z",
  "message": "HelmApp upgrade failed: error='failed to create resource: configmaps \"acme-messaging-fc4bwd8-readinessprobe\" is forbidden: exceeded quota: quota-account, requested: count/configmaps=1, used: count/configmaps=15, limited: count/configmaps=15', values='{\"admin\":{\"domain\":\"acme-messaging-fc4bwd8\", ... }'",
  "observedGeneration": 1,
  "reason": "UpgradeFailed",
  "status": "False",
  "type": "Released"
}
```

If needed, drill down to the Helm revisions associated with the domain by using the below commands.

```sh
helm history $RELEASE_NAME
```
