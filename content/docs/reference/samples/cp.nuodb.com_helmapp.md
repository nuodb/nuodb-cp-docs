---
title: "HelmApp"
description: "A sample HelmApp object with fields documented"
summary: ""
draft: false
weight: 957
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
apiVersion: cp.nuodb.com/v1
# Standard Kubernetes Kind declaration.
kind: HelmApp
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-helmapp
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the HelmApp.
spec:
  # Source defines the Helm chart location.
  source:
    # The Helm chart name available in the remote repository.
    name: string
    # A https URL to a Helm repo to download the chart from.
    repository: string
    # The version of the chart or semver constraint of the chart to find.
    version: 7.0.2
```

## Extended example

```yaml
# Standard Kubernetes API Version declaration.
apiVersion: cp.nuodb.com/v1
# Standard Kubernetes Kind declaration.
kind: HelmApp
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-helmapp
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the HelmApp.
spec:
  # Source defines the Helm chart location.
  source:
    # The Helm chart name available in the remote repository.
    name: string
    # Whether to pin the Helm chart version to the latest version currently
    # available in the Helm repository so that future reconciliations doesn't
    # automatically pick up new Helm chart version. This is used only if the
    # Helm chart version is set to empty string ("") which represents the
    # user's intent to use the latest chart version.
    pinLatestVersion: true
    # A https URL to a Helm repo to download the chart from.
    repository: string
    # The version of the chart or semver constraint of the chart to find.
    version: 7.0.2
  # Template provides additional configuration for the Helm release.
  template:
    # The backoff duration in seconds after failed helm install/upgrade. The
    # total backoff interval will be multiplied by the number of failures.
    backOffSec: 60
    # Defines what happens with the persistent volume claims after the Helm
    # release is uninstalled. Defaults to 'Delete' which means that all
    # associated PVCs are removed.
    dataRetentionPolicy: Delete
    # Maximum number of retries that should be attempted on failures before
    # giving up. Defaults to 20. Set to negative number to disable retries.
    maxRetries: 20
    # The target namespace to install the Helm release in
    namespace: default
    # The name of the Helm release
    releaseName: string
  # ValuesRefs are references to ConfigMap or Secret resources in the local
  # namespace to check for user-supplied Helm values.
  valuesRefs:
  -
    # DataKey is the data key where the a specific value can be
    # found at. Defaults to "data"
    dataKey: data
    # Kind of the values referent, valid values are ('Secret', 'ConfigMap').
    kind: Secret
    # Name of the values referent. Should reside in the same namespace as the
    # referring resource.
    name: string
# Current observed status of the HelmApp.
status:
  # Components holds information about the observed status of the HelmApp
  # components.
  components:
    # Last update timestamp for this status.
    lastUpdateTime: 2025-11-11T21:30:40.971508Z
    # Workloads define the observed status for all statefulsets and deployments
    # installed by this HelmApp.
    workloads:
    -
      # Group defines the schema of this representation of an object.
      group: string
      # Kind is a string value representing the REST resource this object represents.
      kind: string
      # A human readable message indicating details about why the resource is in
      # this condition
      message: string
      # Name is the resource
      name: string
      # ReadyReplicas is the number of pods created for this resource with a
      # Ready Condition.
      readyReplicas: 1
      # Replicas is the number of pods created by the resource controller.
      replicas: 1
      # The state of the resource
      state: string
      # Version defines the schema version of this representation of an object.
      version: 7.0.2
  # Conditions holds the conditions for the HelmApp.
  conditions:
  -
    # lastTransitionTime is the last time the condition transitioned from one status to another.
    # This should be when the underlying condition changed.  If that is not known, then using the time when the API field changed is acceptable.
    lastTransitionTime: 2025-11-11T21:30:40.971508Z
    # message is a human readable message indicating details about the transition.
    # This may be an empty string.
    message: string
    # observedGeneration represents the .metadata.generation that the condition was set based upon.
    # For instance, if .metadata.generation is currently 12, but the .status.conditions[x].observedGeneration is 9, the condition is out of date
    # with respect to the current state of the instance.
    observedGeneration: 1
    # reason contains a programmatic identifier indicating the reason for the condition's last transition.
    # Producers of specific condition types may define expected values and meanings for this field,
    # and whether the values are considered a guaranteed API.
    # The value should be a CamelCase string.
    # This field may not be empty.
    reason: string
    # status of the condition, one of True, False, Unknown.
    status: True
    # type of condition in CamelCase or in foo.example.com/CamelCase.
    type: string
  # Release holds status information about the Helm release associated with
  # the resource.
  release:
    # Failures is the reconciliation failure count against the latest desired
    # state. It is reset after a successful reconciliation
    failures: 1
    # The chart version used in the last reconciliation attempt
    lastAttemptedChartVersion: string
    # The SHA1 checksum of the values used in the last reconciliation attempt
    lastAttemptedValuesChecksum: string
    # The revision of the last successful Helm release
    lastReleaseRevision: 1
    # The last observed generation.
    observedGeneration: 1
```
