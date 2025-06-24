---
title: "DomainComponentUnreadyReplicas"
description: ""
summary: ""
date: 2025-06-05T13:52:09+03:00
lastmod: 2025-06-05T13:52:09+03:00
draft: false
weight: 105
toc: true
seo:
  title: "" # custom title (optional)
  description: "Domain resource has replicas which were declared to be unready" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

## Meaning

Domain component has unready replicas.

{{< details "Full context" open >}}
Domain resource has replicas which were declared to be unready.
Domain component impacted by this alert is NuoDB Admin Process (AP).
For example, it is expected for a domain to have 3 AP replicas, but it has less than that for a noticeable period of time.
{{< /details >}}

### Symptom

To manually evaluate the conditions for this alert follow the steps below.

A domain, which has a component with unready replicas, will have the `Ready` status condition set to `False`.
List all unready domains.

```sh
JSONPATH='{range .items[*]}{@.metadata.name}:{range @.status.conditions[?(@.type=="Ready")]}{@.type}={@.status}{"\n"}{end}{end}'
kubectl get domain -o jsonpath="$JSONPATH" | grep "Ready=False"
```

Inspect the domain component status and compare the `replicas` and `readyReplicas` fields.

```sh
kubectl get domain <name> -o jsonpath='{.status.components.admins}' | jq
```

## Impact

Service degradation or unavailability.

The NuoDB domain is fault-tolerant and remains available even if a certain number of APs are down.
If half of the APs go down unexpectedly, this impacts the ability to commit Raft commands such as performing domain configuration changes and starting database processes.

The APs perform load-balancing for SQL connections to Transaction Engines (TEs) which are not in `UNKNOWN` state. Unavailable APs might impact obtaining new SQL connections for all databases in the domain.

{{< callout context="note" title="Note" icon="outline/info-circle" >}}
For more information on NuoDB Admin quorum, see [Admin Process (AP) Quorum](https://doc.nuodb.com/nuodb/latest/domain-admin/admin-process-quorum/) and [Admin Scale-down with Kubernetes Aware Admin](https://doc.nuodb.com/nuodb/latest/deployment-models/kubernetes-environments/kubernetes-aware-admin/#admin-scaledown).
{{< /callout >}}

## Diagnosis

- Check the domain state using `kubectl describe domain <name>`.
- Check the domain component state and message.
- Check how many replicas are declared for this component.
- List and check the status of all pods associated with the domain's Helm release.
- Check if there are issues with provisioning or attaching disks to pods
- Check if the cluster-autoscaler is able to create new nodes.
- Check pod logs and identify issues during AP startup
- Check the NuoDB process state.
Kubernetes readiness probes require that the APs are in `Connected` state and caught up with the Raft leader.

### Scenarios

{{< details "Scenario 1: Pod in `Pending` status for a long time" >}}

Possible causes for a Pod not being scheduled:

- A container on the Pod requests a resource not available in the cluster
- The Pod has affinity rules that do not match any available worker node
- One of the containers mounts a volume provisioned in the availability zone (AZ) where no Kubernetes worker is available
- A Persistent volume claim (PVC) created for this Pod has a storage class that may be misconfigured or unusable

{{< /details >}}

{{< details "Scenario 2: AP fails to join the domain" >}}

Upon startup, the AP communicates with its peers to join the domain and receives the domain state from the Raft leader.
For more information, check [Admin Process Peering](https://doc.nuodb.com/nuodb/latest/domain-admin/admin-process/#_admin_process_ap_peering).

Possible causes for unsuccessful startup during this phase are:

- Network issues prevent communication between the AP and its peers
- Incorrect initial domain membership or `peer` configuration

{{< /details >}}

### Example

Get the domain name and its namespace from the alert's labels.
Inspect the domain state in the Kubernetes cluster.

```sh
kubectl get domain acme-messaging -n nuodb-cp-system
```

Notice that the `READY` status condition is `False` which means that the domain is in a degraded state.

```text
NAME             TIER       VERSION   READY   SYNCED   DISABLED   AGE
acme-messaging   n0.small   6.0.2     False   True     False      46h
```

Inspect the domain components state.

```sh
kubectl get domain acme-messaging -o jsonpath='{.status.components}' | jq
```

The output below indicates issues with scheduling `acme-messaging-fc4bwd8-2` Pod because the `acme-messaging-fc4bwd8-2-eph-volume` volume is not provisioned by the persistent volume controller.
The mismatch between `replicas` and `readyReplicas` for this component triggers this alert.

```json
{
  "admins": [
 {
      "kind": "StatefulSet",
      "message": "pod/acme-messaging-fc4bwd8-2: 0/1 nodes are available: waiting for ephemeral volume controller to create the persistentvolumeclaim \"acme-messaging-fc4bwd8-2-eph-volume\". preemption: 0/1 nodes are available: 1 Preemption is not helpful for scheduling.",
      "name": "acme-messaging-fc4bwd8",
      "readyReplicas": 2,
      "replicas": 3,
      "state": "NotReady",
      "version": "v1"
 }
 ],
  "lastUpdateTime": "2025-06-06T14:14:57Z"
}
```

If needed, drill down to the Pod and PVC resources associated with the domain by using the below command.

```sh
RELEASE_NAME=$(kubectl get domain acme-messaging -o jsonpath='{.spec.template.releaseName}')
kubectl get pods,pvc -l release=$RELEASE_NAME
```

Obtain NuoDB domain state by running [nuocmd show domain](https://doc.nuodb.com/nuodb/latest/reference-information/command-line-tools/nuodb-command/nuocmd-reference/#show-domain) inside any NuoDB pod that has `Running` status.

```sh
ADMIN_POD=$(kubectl get pod \
 -l release=${RELEASE_NAME},component=admin \
  --field-selector=status.phase==Running \
 -o jsonpath='{.items[0].metadata.name}')

kubectl exec -ti $ADMIN_POD -- nuocmd show domain
```
