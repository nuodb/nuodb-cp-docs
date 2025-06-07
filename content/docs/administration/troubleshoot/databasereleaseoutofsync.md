---
title: "DatabaseReleaseOutOfSync"
description: ""
summary: ""
date: 2025-06-05T13:52:09+03:00
lastmod: 2025-06-05T13:52:09+03:00
draft: false
weight: 110
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

## Meaning

Database release is out of sync.

{{< details "Full context" open >}}
Database resource desired state is out of sync.
The corresponding database Helm release install/upgrade operation failed to apply the latest Helm values.
{{< /details >}}

## Impact

Latest database configuration is not enforced.

A new database won't become available.
Connectivity to already available databases is not impacted by this issue, however, some features that require applying database configuration changes might be unavailable (e.g. start/stop database, TLS, and DBA password rotation, etc.).

## Diagnosis

- Check the database state using `kubectl describe database <name>`.
- Check the database `Released` condition's state and message.
- Check the `Released` condition's state and message for the corresponding _HelmApp_ resource.
- List the Helm revisions for the Helm release associated with the database.
- Check the latest Helm values for the failed Helm release.
- Check that Helm chart repository services are available.
By default, the public NuoDB Helm charts [repository](https://nuodb.github.io/nuodb-helm-charts) in GitHub is used, however, this can be overridden.

### Scenarios

{{< details "Symptom 1: Helm charts repository not available" >}}

The NuoDB operator fails to reach the Helm chart repository and reports the following error:

```text
unable to fetch chart:
 unable to resolve chart:
 looks like \"http://nuodb-helm-repo\" is not a valid chart repository or cannot be reached
```

Possible causes for Helm repository unreachable:

- Public Helm repository has an outage
- Private Helm in-cluster repository is not running
- Helm repository URL is incorrect
- Authentication is required to allow access to Helm repository

{{< /details >}}

{{< details "Symptom 2: Helm chart name or version are not found" >}}

The NuoDB operator fails to download the Helm chart and reports the following error:

```text
unable to fetch chart:
 unable to resolve chart:
 chart \"database\" version \"3.99.0\" not found in http://nuodb-helm-repo repository
```

Possible causes for Helm chart not found:

- Helm chart name or version is incorrect
- Helm repository URL is incorrect

{{< /details >}}

{{< details "Symptom 3: Helm chart resource create/update failure" >}}

Helm operations are targeting the Kubernetes API server directly.
Kubernetes API server and admission controllers are validating incoming resources and any errors will result in failure of the entire Helm operation.
NuoDB Control Plane (CP) enforces extensive validation on NuoDB resources to prevent invalid configuration, however, there are other factors that result in Helm operation errors.

Possible causes for resource creation/update failure:

- Kubernetes API server is not available
- Configured admission controller is unavailable and validation/mutation webhooks can't be executed
- The NuoDB operator doesn't have required RBAC permissions to create resources of a specific group-kind
- There is a _ResourceQuota_ which limits a specific resource
- A resource immutable field is updated during `helm upgrade` operation

{{< /details >}}

{{< callout context="caution" title="Exhausting resource sync attemts" icon="outline/alert-triangle" >}}

NuoDB operator will retry failed Helm operations with the configured retry count (`20` by default) and increasing backoff (starting at `60s` by default).
Once the retries are exhausted, the Helm operation reconciliation will be suspended.
To re-activate Helm release reconciliation for such resources after the root cause is fixed, see [Reset Helm operation attempts](#reset-helm-operation-attempts).

{{< /callout >}}

### Example

Get the database name and its namespace from the alert's labels.
Inspect the database state in the Kubernetes cluster.

```sh
kubectl get database acme-messaging-demo -n nuodb-cp-system
```

Notice that the `SYNCED` value is `False` which means that the database desired state is not enforced.

```text
NAME                  TIER       VERSION   READY   SYNCED   DISABLED   AGE
acme-messaging-demo   n0.small   6.0.2     False   False    False      62h
```

Inspect the database `Released` condition.

```sh
kubectl get database acme-messaging-demo -o jsonpath='{.status.conditions[?(@.type=="Released")]}' | jq
```

The output below indicates issues with the corresponding `acme-messaging-demo-zfb77wc` release because an existing _ResourseQuota_ limits creation of the Helm values Secret resource.
This failure happens even before invoking the Helm operation.

```json
{
  "lastTransitionTime": "2025-06-10T09:32:08Z",
  "message": "failed to reconcile database release acme-messaging-demo-zfb77wc: unable to process Secret default/acme-messaging-demo-zfb77wc-values: secrets \"acme-messaging-demo-zfb77wc-values\" is forbidden: exceeded quota: quota-account, requested: count/secrets=1, used: count/secrets=782, limited: count/secrets=782",
  "observedGeneration": 1,
  "reason": "ReconciliationFailed",
  "status": "False",
  "type": "Released"
}
```

If needed, drill down to the _HelmApp_ resources and Helm revisions associated with the database by using the below commands.

```sh
RELEASE_NAME=$(kubectl get database acme-messaging-demo -o jsonpath='{.spec.template.releaseName}')
kubectl describe helmapp $RELEASE_NAME
helm history $RELEASE_NAME
```

To inspect Helm supplied during Helm operation, execute:

```sh
kubectl get secret "${RELEASE_NAME}-values" -o jsonpath='{.data.values}' | base64 -d
```

To inspect Helm values associated with a particular Helm release, execute:

```sh
helm get values $RELEASE_NAME
```

### Reset Helm operation attempts

Validate that the _HelmApp_ retries are exhausted.

```sh
RELEASE_NAME=$(kubectl get database acme-messaging-demo -o jsonpath='{.spec.template.releaseName}')
kubectl get helmapp $RELEASE_NAME -o jsonpath='{.status.conditions[?(@.type=="Released")]}' | jq
```

Notice that the `Released` condition has `RetriesExhausted` reason meaning that Helm release reconciliation won't be retried anymore.

```json
{
  "reason": "RetriesExhausted",
  "status": "False",
  "type": "Released"
}
```

Reset the failure count by patching the status sub-resource.

```sh
kubectl patch helmapp $RELEASE_NAME \
 --type merge \
  --subresource status \
 -p '{"status": {"release": {"failures": 0}}}'
```
