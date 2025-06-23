---
title: "DatabaseComponentUnreadyReplicas"
description: "Database resource has a component with replicas which were declared to be unready"
summary: ""
date: 2025-06-05T13:52:09+03:00
lastmod: 2025-06-05T13:52:09+03:00
draft: false
weight: 100
toc: true
seo:
  title: "" # custom title (optional)
  description: "Database resource has a component with replicas which were declared to be unready" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

## Meaning

Database component has unready replicas.

{{< details "Full context" open >}}
Database resource has a component with replicas which were declared to be unready.
Database components impacted by this alert are Transaction Engines (TEs) and Storage Managers (SMs).
For example, it is expected for a database to have 2 TE replicas, but it has less than that for a noticeable period of time.

On rare occasions, there may be more replicas than request and the system did not clean them up.
{{< /details >}}

### Symptom

To manually evaluate the conditions for this alert follow the steps below.

Database which has a component with unready replicas will have the `Ready` status condition set to `False`.
List all unready databases.

```sh
JSONPATH='{range .items[*]}{@.metadata.name}:{range @.status.conditions[?(@.type=="Ready")]}{@.type}={@.status}{"\n"}{end}{end}'
kubectl get database -o jsonpath="$JSONPATH" | grep "Ready=False"
```

Inspect the database component status and compare the `replicas` and `readyReplicas` fields.

```sh
kubectl get database <name> -o jsonpath='{.status.components}' | jq
```

## Impact

Service degradation or unavailability.

NuoDB database is fault-tolerant and remains available even if a certain number of database processes are down.
Depending on the database configuration, however, this might have an impact on the database availability of certain data partitions (storage groups) or client applications using custom load-balancing rules.

## Diagnosis

- Check the database state using `kubectl describe database <name>`.
- Check the database component state and message.
- Check how many replicas are declared for this component.
- List and check the status of all pods associated with the database's Helm release.
- Check if there are issues with provisioning or attaching disks to pods
- Check if the cluster-autoscaler is able to create new nodes.
- Check pod logs and identify issues during database process startup
- Check the NuoDB process state.
Kubernetes readiness probes require that the database processes are in `MONITORED:RUNNING` state.

### Scenarios

{{< details "Scenario 1: Pod in `Pending` status for a long time" >}}

Possible causes for a Pod not being scheduled:

- A container on the Pod requests a resource not available in the cluster
- The Pod has affinity rules that do not match any available worker node
- One of the containers mounts a volume provisioned in an availability zone (AZ) where no Kubernetes worker is available

{{< /details >}}

{{< details "Scenario 2: Pod in `CreateContainerConfigError` status for a long time" >}}

Possible causes for a container not being created:

- The container depends on a resource that does not exist yet (e.g. ConfigMap or Secret)
- NuoDB Control Plane external operator did not populate the database connection details yet

{{< /details >}}

{{< details "Scenario 3: Database process fails to join the domain" >}}

Upon startup, the main _engine_ container process communicates with the NuoDB Admin to register the database process with the domain and start it using the NuoDB binary.

Possible causes for unsuccessful startup during this phase are:

- Network issues prevent communication between the container entrypoint client scripts and NuoDB Admin REST API
- The NuoDB Admin layer is not available or has no Raft leader
- No Raft quorum in the NuoDB Admin prevents committing new Raft commands
- AP with ordinal 0 formed a separate domain. In case of catastrophic loss of the `admin-0` container (i.e. its durable domain state `raftlog` file is lost), it might form a new domain causing a split-brain scenario. For more information, see [Setting _bootstrapServers_ Helm value](https://github.com/nuodb/nuodb-helm-charts/blob/v3.10.0/stable/admin/values.yaml#L106).

{{< /details >}}

{{< details "Scenario 4: Database process fails to join the database" >}}

Once started, a database process communicates with the rest of the database and executes an entry protocol.

Possible causes for unsuccessful startup during this phase are:

- Network issues prevent communication between NuoDB database processes
- No suitable entry node is available
- The database process binary version is too old

{{< /details >}}

{{< details "Scenario 5: An SM in `TRACKED` state for a long time" >}}

The database state might be `AWAITING_ARCHIVE_HISTORIES_MSG` indicating that the database leader assignment is in progress.
NuoDB Admin must collect archive history information from all provisioned archives on database cold start.
This requires all SM processes to start and connect to the NuoDB Admin within the configured timeout period.

Possible causes for unsuccessful leader assignment:

- Not all SMs have been scheduled by Kubernes or not all SM processes have started
- Some of the SM pods are in `CrashLoopBackOff` state with long back-off
- There is a _defunct_ archive metadata provisioned in the domain which is not served by an actual SM

{{< /details >}}

{{< details "Scenario 6: An TE in `TRACKED` state for a long time" >}}

A TE process joins the database via an entry node which is normally the first SM that goes to `RUNNING` state.
NuoDB Admin performs synchronization tasks so that TEs are started after the entry node is available.

Possible causes for missing entry node:

- Database leader assignment is not performed after cold start. See _Symptom 5_
- The `UNPARTITIONED` storage group is not in `RUNNING` state

{{< /details >}}

{{< details "Scenario 7: SM in `CONFIGURED:RECOVERING_JOURNAL` state for a long time" >}}

Upon startup, SM processes perform a journal recovery.
This may be time consuming if there are many journal entries to recover.
The SM process reports the progress of the journal recovery which is displayed in `nuocmd show domain` output.

Possible causes for slow journal recovery:

- High latency of the archive disk caused by reaching the IOPS limit

{{< /details >}}

### Example

Get the database name and its namespace from the alert's labels.
Inspect the database state in the Kubernetes cluster.

```sh
kubectl get database acme-messaging-demo -n nuodb-cp-system
```

Notice that the `READY` status condition is `False` which means that the database is in a degraded state.

```text
NAME                  TIER       VERSION   READY   SYNCED   DISABLED   AGE
acme-messaging-demo   n0.small   6.0.2     False   True     False      46h
```

Inspect the database components state.

```sh
kubectl get database acme-messaging-demo -o jsonpath='{.status.components}' | jq
```

The output below indicates issues with scheduling `te-acme-messaging-demo-zfb77wc-5cd8b5f7c4-qnplm` Pod because of insufficient memory on the cluster.
The mismatch between `replicas` and `readyReplicas` for this component triggers this alert.

```json
{
  "lastUpdateTime": "2025-06-06T13:08:19Z",
  "storageManagers": [
 {
      "kind": "StatefulSet",
      "name": "sm-acme-messaging-demo-zfb77wc",
      "readyReplicas": 2,
      "replicas": 2,
      "state": "Ready",
      "version": "v1"
 }
 ],
  "transactionEngines": [
 {
      "kind": "Deployment",
      "message": "there is an active rollout for deployment/te-acme-messaging-demo-zfb77wc; pod/te-acme-messaging-demo-zfb77wc-5cd8b5f7c4-qnplm: 0/1 nodes are available: 1 Insufficient memory. preemption: 0/1 nodes are available: 1 No preemption victims found for incoming pod.",
      "name": "te-acme-messaging-demo-zfb77wc",
      "readyReplicas": 5,
      "replicas": 6,
      "state": "Updating",
      "version": "v1"
 }
 ]
}
```

If needed, drill down to the Pod resources associalted with the database by using the below command.

```sh
RELEASE_NAME=$(kubectl get database acme-messaging-demo -o jsonpath='{.spec.template.releaseName}')
kubectl get pods -l release=$RELEASE_NAME
```

Obtain NuoDB domain state by running [nuocmd show domain](https://doc.nuodb.com/nuodb/latest/reference-information/command-line-tools/nuodb-command/nuocmd-reference/#show-domain) and [nuocmd show database](https://doc.nuodb.com/nuodb/latest/reference-information/command-line-tools/nuodb-command/nuocmd-reference/#show-domain) inside any NuoDB pod that has `Running` status.

```sh
SM_POD=$(kubectl get pod \
 -l release=${RELEASE_NAME},component=sm \
  --field-selector=status.phase==Running \
 -o jsonpath='{.items[0].metadata.name}')

kubectl exec -ti $SM_POD -- nuocmd show domain
```
