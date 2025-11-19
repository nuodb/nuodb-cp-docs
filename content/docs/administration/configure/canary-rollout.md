---
title: "Rollout Configuration Changes"
description: ""
summary: ""
date: 2025-10-21T09:30:00+03:00
lastmod: 2025-10-21T09:30:00+03:00
draft: false
weight: 255
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

NuoDB DBaaS manages NuoDB databases at scale and automates certain aspects of the database lifecycle.
[Service tiers]({{< ref "./service-tiers.md" >}}) are a small set of DBaaS administrator-managed, predefined database configuration profiles that expose fully supported and documented settings.
Because these tiers are shared across many databases, any modification to a tier triggers a large number of resulting upgrades.
A change in a service tier will be propagated immediately to all databases that reference this tier at the same time.
This can be potentially disruptive even if the configuration change made is correct, and catastrophic if the change is incorrect.
To manage this safely, cluster administrators control how these changes are rolled out, using canary deployment strategies to introduce updates gradually and with minimal risk.

NuoDB DBaaS supports delivering configuration changes progressively to domain and database resources.
This allows configuration updates to be delivered in a controlled way defined by NuoDBaaS operations best practices and enforced using rollout templates.

## Canary rollout

The `CanaryRollout` custom resource is a job for rolling out a change progressively to a group of `Domain` and `Database` resources.
A [JSON merge patch](https://datatracker.ietf.org/doc/html/rfc7386) represents the desired configuration change to resources matched by a label selector.
The canary rollout is either created automatically by the system, manually using `kubectl`, or via REST API [/cluster/canaryrollouts](https://nuodb.github.io/nuodb-cp-releases/api-doc/#put-/cluster/canaryrollouts/-name-) cluster-scoped resource.

## Canary rollout template

The `CanaryRolloutTemplate` custom resource is a reusable configuration defining the rollout strategy.
It is referenced by a `CanaryRollout` resource, and together they describe how a specific configuration change is delivered to selected targets.

Each template defines steps executed sequentially.
If any of the steps fail, the canary rollout is stopped and marked as failed.

### Promote step

The [promote step]({{< ref "../../reference/cp.nuodb.com.md#promotetorolloutstep" >}}) defines the target resources to which a change is promoted in parallel and the rollback behaviour in case of failed analysis.
Various selectors and filters limit the promoted targets, such as label selector, number of targets, percentage of total targets, etc.

{{< callout context="note" title="Note" icon="outline/info-circle" >}}
There is no implicit _promote_ step for canary templates.
For a change to be propagated to a specific target, the target must match one of the explicitly configured _promote_ steps.
{{< /callout >}}

### Analysis step

The [analysis step]({{< ref "../../reference/cp.nuodb.com.md#canaryrolloutanalysis" >}}) defines the type of analysis run to be performed on target resources after a change has been rolled out.
An analysis run is executed in parallel on all targets promoted from the last _promote_ step.
If at least one analysis run fails for some of the targets, the canary rollout is stopped.
Multiple analysis runs may be defined globally and executed after each _promote_ step.

### Pause step

The [pause step]({{< ref "../../reference/cp.nuodb.com.md#pauserolloutstep" >}}) defines the duration for which the canary rollout will be paused.
A zero (0) duration pause the rollout until it is manually approved.

To manually resume a paused canary rollout, update the `Paused` condition reason to `CanaryManuallyApproved` using `kubectl` directly or through the REST API.

{{< tabs "approve-paused-rollout" >}}
{{< tab "nuodb-cp" >}}

```sh
nuodb-cp httpclient PATCH cluster/canaryrollouts/acme-upgrade \
  --query-param updateStatus=true \
  -d '[{
    "op": "replace",
    "path": "/status/conditions",
    "value": [{
    "type": "Paused",
    "status": "True",
    "reason": "CanaryManuallyApproved",
    "message": "",
    "lastTransitionTime": "'$(date +"%Y-%m-%dT%H:%M:%SZ")'"
  }]}]'
```

{{< /tab >}}
{{< tab "kubectl" >}}

```sh
kubectl patch canaryrollout <name> \
 --subresource status \
  --type merge \
  --patch '{"status": {"conditions": [{
      "type": "Paused",
      "status": "True",
      "reason": "CanaryManuallyApproved",
      "message": "",
      "lastTransitionTime": "'$(date +"%Y-%m-%dT%H:%M:%SZ")'"
  }]}}'
```

{{< /tab >}}
{{< /tabs >}}

## Monitoring rollout progress

The NuoDB Operator creates Kubernetes events for the canary rollout execution trace.
Use `kubectl events --for canaryrollout/<name>` to monitor the status of the rollout.

An example canary rollout execution log is available below.

```text
LAST SEEN   TYPE     REASON                       OBJECT                       MESSAGE
22m         Normal   CanaryPauseStep              CanaryRollout/acme-upgrade   Pause step (1/13) activated: canary rollout paused until manual approval
21m         Normal   CanaryManuallyApproved       CanaryRollout/acme-upgrade   Pause step (1/13) manually approved after 55s
21m         Normal   Progressing                  CanaryRollout/acme-upgrade   Step (1/13) completed
21m         Normal   CanaryPromoteStep            CanaryRollout/acme-upgrade   Promote step (2/13) progressing target Domain default/acme-messaging
21m         Normal   CanaryPromoteStep            CanaryRollout/acme-upgrade   Promote step (2/13) progressing target Database default/acme-messaging-demo
16m         Normal   CanaryAnalysisRunSucceeded   CanaryRollout/acme-upgrade   Analysis step (2/13) analysis "ready" succeed for target Domain default/acme-messaging
16m         Normal   CanaryAnalysisRunSucceeded   CanaryRollout/acme-upgrade   Analysis step (2/13) analysis "ready" succeed for target Database default/acme-messaging-demo
16m         Normal   Progressing                  CanaryRollout/acme-upgrade   Step (2/13) completed
16m         Normal   CanaryPromoteStep            CanaryRollout/acme-upgrade   Promote step (3/13) matches no targets
16m         Normal   Progressing                  CanaryRollout/acme-upgrade   Step (3/13) completed
16m         Normal   CanaryPauseStep              CanaryRollout/acme-upgrade   Pause step (4/13) activated: canary rollout paused for 5m0s
11m         Normal   CanaryPauseStep              CanaryRollout/acme-upgrade   Pause step (4/13) resuming rollout after 5m1s
11m         Normal   Progressing                  CanaryRollout/acme-upgrade   Step (4/13) completed
11m         Normal   CanaryPromoteStep            CanaryRollout/acme-upgrade   Promote step (5/13) matches no targets
...
```

The current state for pending analysis runs is recorded for each promoted target in `status.lastPromotedTargets[*].analysisRuns`.

{{< callout context="note" title="Note" icon="outline/info-circle" >}}
Since canary rollouts may run for an extended time before completion, it is recommended to collect and store Kubernetes events in an external system (e.g., Grafana Loki) for long-term storage.
{{< /callout >}}

## Use cases

The canary rollout resources are the main building blocks for delivering any change to multiple Kubernetes resources progressively.
A typical use case is updating the version of sorftware deliverables such as NuoDB product or Helm chart version, configuration revision or a combination of these.
This section describes different approaches to utilize canary rollouts in your NuoDB DBaaS deployments.

### Changes in service tiers

The NuoDB service tiers and Helm features are versioned resources, which means that a configuration history is maintained for them by the NuoDB operator.
A new configuration version, called _revision_, is created on every update of the resource's desired specification.
Configuration revisions are referenced in other resources, such as the domain or database.
If an explicit revision is not pinned in a reference, then the _latest_ revision is used.
A revision that is not in use or is not the _latest_ is automatically removed from the version history.
For example, a new service tier revision is created when either a service tier's desired specification is modified or a referenced Helm feature's desired spec is modified.

Keeping version history of shared configuration and explicitly referencing these revisions allows decoupling the database lifecycle from the configuration lifecycle.
NuoDB DBaaS supports both manual and automatic revision rollout to selected target resources.

To enable automatic rollout of service tier revisions, set the `spec.updateStrategy.type` field to `CanaryRollout` and configure the `CanaryRolloutTemplate` custom resource reference in `spec.updateStrategy.canary.templateRef.name`.
If enabled, the NuoDB operator manages the lifecycle of `CanaryRollout` resources, automatically rolling out new service tier revisions to all Domain and Database resources that reference them.

{{< callout context="note" title="Note" icon="outline/info-circle" >}}
The _nuodb-cp-config_ Helm chart enables automatic rollout for all standard service tiers by exposing the `cpConfig.service.type.updateStrategy.type` and `cpConfig.service.type.updateStrategy.canary.template` Helm values.
{{< /callout >}}

The diagram below illustrates a successful automatic configuration rollout triggered by a change in a Helm feature.
The example is simplified and has one Helm feature, one service tier, and two databases for demonstration purposes.
Multiple controllers in the NuoDB operator are responsible for progressively rolling out the change in the Helm feature to both databases.

{{< figure src="canary-success-flow.png" caption="Figure 1. Canary rollout success flow" alt="Canary rollout success flow" >}}

In case the analysis defined in the `CanaryRolloutTemplate` fails for one or more target databases, the rollout will stop, and the impacted databases will be rolled back to the previous service tier revision.

{{< callout context="note" title="Note" icon="outline/info-circle" >}}
Depending on the canary template configuration, multiple databases may be updated at once.
By default, a rollback will be performed only for the databases with failed analysis.
{{< /callout >}}

{{< figure src="canary-rollback-flow.png" caption="Figure 2. Canary rollout rollback flow" alt="Canary rollout rollback flow" >}}

### Example: Service tier rollout

The below canary template defines a progressive rollout strategy for service tier change to 2, 10%, 40% and 100% of domains and databases with _prod_ SLA.
After each promotion, the rollout will make sure that the resources are _synced_ and _ready_ by running status condition analysis.

```yaml
apiVersion: cp.nuodb.com/v1beta1
kind: CanaryRolloutTemplate
metadata:
  name: example-tier-update
spec:
  analysis:
  - name: "ready"
    interval: 5m
    checkStatusCondition:
      type: Ready
      status: "True"
      timeout: 15m
  - name: "synced"
    interval: 1m
    checkStatusCondition:
      type: Released
      status: "True"
      timeout: 5m
  steps:
  # Promote to 2 PROD domains/databases
  - promoteTo:
      labelSelector:
        matchLabels:
          cp.nuodb.com/sla: prod
      limitCount: 2

  # Promote to 10% of the PROD domains/databases
  - promoteTo:
      labelSelector:
        matchLabels:
          cp.nuodb.com/sla: prod
      limitPercentage: 10

  # Promote to 40% of the PROD domains/databases
  - promoteTo:
      labelSelector:
        matchLabels:
          cp.nuodb.com/sla: prod
      limitPercentage: 40

  # Promote to the rest of the domains/databases
  - promoteTo: {}
```

### Helm charts version rollout

The [automatic configuration rollout](#changes-in-service-tiers) updates the service tier revision reference in all promoted resources only.
The NuoDB Helm chart version used to deploy the NuoDB workloads stays unchanged.
This means that the new revision of the shared configuration must be backwards compatible with older versions of NuoDB Helm charts.
Optional [Helm features]({{< ref "service-tiers.md#database-configuration" >}}) with Helm chart version constraints can help with this task; however, sometimes supporting backwards compatibility is hard or not desired.

{{< callout context="note" title="Note" icon="outline/info-circle" >}}
NuoDB Helm chart version is upgraded implicitly every time the NuoDB product version is upgraded or when the `productVersion` field is omitted from the project/database payload via REST API.
The `nuodb-cp-helm-versions` ConfigMap allows administrators to configure the default Helm chart versions used by the REST service per _SLA_.
{{< /callout >}}

Canary rollouts are a convenient way to perform explicit NuoDB Helm charts version upgrades across multiple domains and databases.

### Example: Helm charts version upgrade

The rollout template is similar to the [previous example](#example-service-tier-rollout).
The below canary rollout will upgrade all targets in _Acme_ organization to the most recent version of the NuoDB Helm chart.

```yaml
apiVersion: cp.nuodb.com/v1beta1
kind: CanaryRollout
metadata:
  name: acme-helm-upgrade-latest
spec:
  patch:
    spec:
      chart:
        version: ""
  rolloutTemplate:
    name: example-tier-update
  selector:
    matchLabels:
      cp.nuodb.com/organization: "acme"
```

### Product version upgrade

Canary rollouts provide a method to promote newer NuoDB product releases with confidence by performing upgrades across selected databases.
DBaaS administrators maintain reusable rollout templates for minor version upgrades.
The operations team references them in a canary rollout job for a specific NuoDB release and monitors its progress across a fleet of databases.

{{< callout context="caution" title="NuoDB protocol version upgrade" icon="outline/alert-triangle" >}}
NuoDB [database protocol version upgrade](https://doc.nuodb.com/nuodb/latest/deployment-models/physical-or-vmware-environments-with-nuodb-admin/installing-nuodb/upgrade-to-a-new-release/upgrade-the-database-protocol/#nav-container-toggle) is not automatically performed when rolling out a new NuoDB version.
On NuoDB major version change, the database protocol upgrade must be planned accordingly and performed as an additional manual step after the update.
It is stongly recommended to take a database backup before NuoDB version upgrade.
{{< /callout >}}

If the new version is promoted to a domain and its databases by the same _promote_ step, the NuoDB operator will ensure that the domain is upgraded before the databases.
This reduces the number of NuoDB processes that are shut down at the same time and reduces the risk of cascading failures.

### Example: Minor product version upgrade

The below canary template defines an upgrade strategy by progressively promoting a new version to two, 30% and 100% of domains and databases with _dev_ SLA.
After the promoted resources are successfully upgraded, the rollout is paused until manual approval.
Once the approval is given, the version is promoted to 2, 10%, 40% and 100% of production domains and databases.

```yaml
apiVersion: cp.nuodb.com/v1beta1
kind: CanaryRolloutTemplate
metadata:
  name: example-version-upgrade
spec:
  skipDisabled: true
  analysis:
  - name: upgrading
      interval: 5s
      checkStatusCondition:
        type: Upgrading
        status: "True"
        timeout: 30m
  steps:
  # Promote to 2 DEV domains/databases
  - promoteTo:
      labelSelector:
        matchLabels:
          cp.nuodb.com/sla: dev
      limitCount: 2
  - analysis:
      name: ready
      interval: 5m
      checkStatusCondition:
        type: Ready
        status: "True"
        timeout: 30m

  # Promote to 2 DEV domains/databases
  - promoteTo:
      labelSelector:
        matchLabels:
          cp.nuodb.com/sla: dev
      limitPercentage: 30
  - analysis:
      name: ready
      interval: 5m
      checkStatusCondition:
        type: Ready
        status: "True"
        timeout: 30m

  # Promote to the rest of DEV domains/databases
  - promoteTo:
      labelSelector:
        matchLabels:
          cp.nuodb.com/sla: dev
  - analysis:
      name: ready
      interval: 5m
      checkStatusCondition:
        type: Ready
        status: "True"
        timeout: 30m

  # Wait until manually approved
  - pause: {}

  # Promote to 2 PROD domains/databases
  - promoteTo:
      labelSelector:
        matchLabels:
          cp.nuodb.com/sla: prod
      limitCount: 2
  - analysis:
      name: ready
      interval: 5m
      checkStatusCondition:
        type: Ready
        status: "True"
        timeout: 30m

  # Promote to 10% of the PROD domains/databases
  - promoteTo:
      labelSelector:
        matchLabels:
          cp.nuodb.com/sla: prod
      limitPercentage: 10
  - analysis:
      name: ready
      interval: 5m
      checkStatusCondition:
        type: Ready
        status: "True"
        timeout: 30m

  # Promote to 40% of the PROD domains/databases
  - promoteTo:
      labelSelector:
        matchLabels:
          cp.nuodb.com/sla: prod
      limitPercentage: 40
  - analysis:
      name: ready
      interval: 5m
      checkStatusCondition:
        type: Ready
        status: "True"
        timeout: 30m

  # Promote to the rest of the domains/databases
  - promoteTo: {}
  - analysis:
      name: ready
      interval: 5m
      checkStatusCondition:
        type: Ready
        status: "True"
        timeout: 30m
```

The template is referenced in the canary rollouts for different versions.
For example, the below canary rollout upgrades all databases in organization _Acme_ to NuoDB v7.0.3.

```yaml
apiVersion: cp.nuodb.com/v1beta1
kind: CanaryRollout
metadata:
  name: acme-upgrade-703
spec:
  patch:
    spec:
      version: 7.0.3
  rolloutTemplate:
    name: example-version-upgrade
  selector:
    matchLabels:
      cp.nuodb.com/organization: "acme"
```
