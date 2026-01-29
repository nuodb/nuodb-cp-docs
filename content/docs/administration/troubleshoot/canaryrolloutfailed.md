---
title: "CanaryRolloutFailed"
description: ""
summary: ""
date: 2025-06-05T13:52:09+03:00
lastmod: 2025-06-05T13:52:09+03:00
draft: false
weight: 483
toc: true
seo:
  title: "" # custom title (optional)
  description: "Canary rollout has failed" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

## Meaning

Canary rollout has failed.

{{< details "Full context" open >}}
A change delivered using a progressive rollout has failed to be enforced on some of the targets.
The canary rollout completed with failure either because the delivered change was incorrect or the configured analysis has failed.
For more information on progressive rollouts, see [Rollout Configuration Changes]({{< ref "../configure/canary-rollout.md" >}}).
{{< /details >}}

### Symptom

To manually evaluate the conditions for this alert, follow the steps below.

A failed canary rollout will have the `Ready` status condition set to `False` and `Complete` status condition set to `True`.
List all failed canary rollouts.

```sh
JSONPATH='{range .items[*]}{@.metadata.name}:{range @.status.conditions[*]}{@.type}={@.status}:{end}{"\n"}{end}'
kubectl get canaryrollout -o jsonpath="$JSONPATH" | grep "Ready=False" | grep "Complete=True" | cut -d':' -f1
```

Inspect the canary `Ready` condition message for more details.

```sh
kubectl get canaryrollout <name> -o jsonpath='{.status.conditions[?(@.type=="Ready")]}' | jq
```

## Impact

The decired change delivered by the canary is not enforced on some targets.
Inspect the `.spec.patch` field to determine if this is a configuration change or NuoDB product version upgrade.
Changes in the service tiers are typically delivered via canary rollouts by updating the tier revision number (e.g. `{"spec":{"type":{"tierRef":{"revision":"2"}}}}`).

By default, all failed targets will be rollbacked automatically to limit the impact of a potentially incorrect change.
The canary rollout will stop immediately after failure for at least one target, which means that the configuration change won't be attempted on the remaining targets.

## Diagnosis

- Check the canary rollout state using `kubectl describe canaryrollout <name>`.
- Check the canary rollout `Ready` condition's state and message.
- Check the canary rollout events as described in [Monitoring rollout progress]({{< ref "../configure/canary-rollout.md#monitoring-rollout-progress" >}})
- Check last promoted targets for failed analysis using `kubectl get canaryrollout <name> -o jsonpath='{.status.lastPromotedTargets}' | jq`
- Diagnose issues with failed databases as described in [Diagnosing database component]({{< ref "databasecomponentunreadyreplicas.md#diagnosis" >}}).
Review historical information recorded in events, logs and metrics because the target database might have been rollbacked already.
- Attempt to perform the change manually on a previously failed database or its cloned copy.
- Retry the canary rollout as described in [Restart rollout]({{< ref "../configure/canary-rollout.md#restart-rollout" >}})

### Scenarios

{{< details "Scenario 1: Target analysis failure" >}}

The canary rollout executes analysis configured in the rollout template against all promoted targets.
If some of the analysis doesn't complete successfully after the predefined timeout, it will be marked as failed.
Currently, there is no way to determine if the target is not ready because of the change promoted by the canary rollout or due to some unrelated reason.

Possible causes for target analysis failure:

- The change delivered by the canary rollout is invalid or incompatible with some targets
- The target was already in a failed state.
The analysis is not run before target promotion and is not a gating condition for delivering a patch to a target.
A target can be unready before and after the patch, which will fail the entire canary rollout.
It is important to monitor and disable domains or databases that are in a failed state for a long time.
Alternatively, such targets must be excluded from canary rollouts by using the canary label selector.
- The analysis timeout is too short for some targets.
Rolling upgrade might take more time for some databases due to the number of engines or the time to perform journal recovery or SYNCING.

{{< /details >}}

### Example

Get the canary rollout name and its namespace from the alert's labels.
Inspect the canary rollout state in the Kubernetes cluster.

```sh
kubectl get canaryrollout n0.nano -n nuodb-cp-system
```

Notice that the `READY` value is `False` and `COMPLETED` is `True`, which means that the canary rollout has failed.

```text
NAME      PAUSED   READY   COMPLETED   ROLLBACKED   AGE
n0.nano   False    False   True        False        6m50s
```

Inspect the canary rollout failure message.

```sh
kubectl get canaryrollout n0.nano -o jsonpath='{.status.conditions[?(@.type=="Ready")]}' | jq
```

```json
{
  "lastTransitionTime": "2026-01-29T09:23:21Z",
  "message": "failed analysis: name=\"ready\", targets=[Database/acme-messaging-drive Database/acme-messaging-store]",
  "observedGeneration": 1,
  "reason": "CanaryAnalysisRunFailed",
  "status": "False",
  "type": "Ready"
}
```

Check the canary rollout events.

```sh
kubectl describe canaryrollout n0.nano
```

The output below shows that a configuration change has been promoted successfully to two databases in step 1, followed by another two databases in step 2.
Both databases in step 2 did not become ready within the configured analysis timeout (in this case 3min).
The "ready" analysis failed for these two targets, and rollback was performed on them to prevent any database downtime.

```text
  Type     Reason                      Age    From               Message
  ----     ------                      ----   ----               -------
  Normal   CanaryPromoteStep           5m22s  nuodb-cp-operator  Promote step (1/4) progressing target Database default/acme-messaging-demo
  Normal   CanaryPromoteStep           5m22s  nuodb-cp-operator  Promote step (1/4) progressing target Database default/acme-messaging-disk
  Normal   CanaryAnalysisRunSucceeded  4m22s  nuodb-cp-operator  Analysis step (1/4) analysis "ready" succeed for target Database default/acme-messaging-demo
  Normal   CanaryAnalysisRunSucceeded  4m22s  nuodb-cp-operator  Analysis step (1/4) analysis "ready" succeed for target Database default/acme-messaging-disk
  Normal   CanaryAnalysisRunSucceeded  4m22s  nuodb-cp-operator  Analysis step (1/4) analysis "synced" succeed for target Database default/acme-messaging-demo
  Normal   CanaryAnalysisRunSucceeded  4m22s  nuodb-cp-operator  Analysis step (1/4) analysis "synced" succeed for target Database default/acme-messaging-disk
  Normal   Progressing                 4m22s  nuodb-cp-operator  Step (1/4) completed
  Normal   CanaryPromoteStep           4m22s  nuodb-cp-operator  Promote step (2/4) progressing target Database default/acme-messaging-drive
  Normal   CanaryPromoteStep           4m22s  nuodb-cp-operator  Promote step (2/4) progressing target Database default/acme-messaging-store
  Normal   CanaryAnalysisRunSucceeded  3m22s  nuodb-cp-operator  Analysis step (2/4) analysis "synced" succeed for target Database default/acme-messaging-drive
  Normal   CanaryAnalysisRunSucceeded  3m22s  nuodb-cp-operator  Analysis step (2/4) analysis "synced" succeed for target Database default/acme-messaging-store
  Warning  CanaryAnalysisRunFailed     81s    nuodb-cp-operator  Analysis step (2/4): analysis "ready" failed for target Database default/acme-messaging-drive: unexpected status for condition Ready expected=True, actual=False: unhealthy components: [transactionEngines]; unhealthy resources: [deployment/te-acme-messaging-drive-fbd7bd9] (timeout after 3m0s)
  Warning  CanaryAnalysisRunFailed     81s    nuodb-cp-operator  Analysis step (2/4): analysis "ready" failed for target Database default/acme-messaging-store: unexpected status for condition Ready expected=True, actual=False: unhealthy components: [transactionEngines]; unhealthy resources: [deployment/te-acme-messaging-store-9dz2w4z] (timeout after 3m0s)
  Warning  CanaryAnalysisRunFailed     81s    nuodb-cp-operator  Step (2/4) failed: failed analysis: name="ready", targets=[Database/acme-messaging-drive Database/acme-messaging-store]
  Normal   RollbackSucceededReason     81s    nuodb-cp-operator  Rollback target Database default/acme-messaging-drive
  Normal   RollbackSucceededReason     81s    nuodb-cp-operator  Rollback target Database default/acme-messaging-store
```

Let's drill down and list the events for one of the failed deployments and its pods.

```sh
kubectl get events  | grep te-acme-messaging-drive-fbd7bd9 | grep Warning
```

```text
6m13s       Warning   CanaryAnalysisRunFailed      canaryrollout/n0.nano                                                               Analysis step (2/4): analysis "ready" failed for target Database default/acme-messaging-drive: unexpected status for condition Ready expected=True, actual=False: unhealthy components: [transactionEngines]; unhealthy resources: [deployment/te-acme-messaging-drive-fbd7bd9] (timeout after 3m0s)
...
9m8s        Warning   FailedScheduling             pod/te-acme-messaging-drive-fbd7bd9-6f69c9ffcf-s5wr2                                0/1 nodes are available: 1 Insufficient cpu. preemption: 0/1 nodes are available: 1 No preemption victims found for incoming pod.
```

The error above indicates not enough CPU available in the cluster to schedule the TE pod.
We suspect that the performed change might have bumped the CPU requests which was fine for the first two databases but eventually the cluster capacity was exhausted.

#### Inspect service tier change

To inspect the canary patch, execute:

```sh
kubectl get canary n0.nano -o jsonpath='{.spec.patch}'
```

The output shows a change in the service tier revision, which means that a change was performed in the service tier or a Helm feature referenced by the service tier.
For more information about shared database configuration, see [Service tiers]({{< ref "../configure/service-tiers.md" >}}).

```json
{"spec":{"type":{"tierRef":{"revision":"100"}}}}
```

To compare service tier and Helm feature revisions, lets create a small utility function.

```bash
diff_revisions() {
  kind_name=$1
  new_rev=$2
  prev_rev=$3
  context=${4:-"3"}

  diff -U ${context} \
    <(kubectl get "$kind_name" \
      -o jsonpath="{range @.status.history.revisions[?(@.generation==${prev_rev})]}{@.spec}{end}" | base64 -d | jq) \
    <(kubectl get "$kind_name" \
      -o jsonpath="{range @.status.history.revisions[?(@.generation==${new_rev})]}{@.spec}{end}" | base64 -d | jq)
}
```

Compare the service tier revision `100` with the previous revision (in this case `99`) using the following command:

```sh
diff_revisions "tier/n0.nano" 100 99
```

```diff
--- /dev/fd/11	2026-01-29 12:15:45
+++ /dev/fd/12	2026-01-29 12:15:45
@@ -62,7 +62,7 @@
     },
     {
       "name": "nano-resources",
-      "revision": "6"
+      "revision": "7"
     },
     {
       "name": "nano-disk",
```

In this case, the revision of `nano-resources` Helm feature is the only change, so it must have been updated.
Let's compare its revisions.

```sh
diff_revisions "feature/nano-resources" 7 6 10
```

```diff
--- /dev/fd/11	2026-01-29 12:16:11
+++ /dev/fd/12	2026-01-29 12:16:11
@@ -27,18 +27,18 @@
         }
       },
       "te": {
         "memoryOption": "500Mi",
         "resources": {
           "limits": {
             "cpu": 8,
             "memory": "500Mi"
           },
           "requests": {
-            "cpu": "2",
+            "cpu": 4,
             "memory": "500Mi"
           }
         }
       }
     }
   }
 }
```

The CPU requests for the TE engine have been increased, which affects all databases using the `n0.nano` service tier.
This aligns with the previous analysis for the database TE pod not being scheduled due to resource constraints.
