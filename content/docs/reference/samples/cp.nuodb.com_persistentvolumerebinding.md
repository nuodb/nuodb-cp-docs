---
title: "PersistentVolumeRebinding"
description: "A sample PersistentVolumeRebinding object with fields documented"
summary: ""
draft: false
weight: 962
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
kind: PersistentVolumeRebinding
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-persistentvolumerebinding
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the PersistentVolumeRebinding.
spec:
  # The rebindings to perform.
  rebindings:
  -
    # If specified, rebinds of a set of PVCs in the source namespace to a
    # set of PVCs in the target namespace. The source namespace is the
    # namespace of the PersistentVolumeRebinding resource, while the target
    # namespace is the namespace that the controller reconciling the
    # PersistentVolumeRebinding resource is running in.
    template:
      # The definition of a set of PVCs in the source namespace.
      sourceClaim:
        # If specified, defines the PVCs to be the archive PVCs for SMs in the
        # supplied database.
        dbaasDatabaseArchive:
          # The name of the database.
          database: string
          # The name of the organization.
          organization: string
          # The name of the project.
          project: string
      # The definition of a set of PVCs in the target namespace.
      targetClaim:
        # If specified, defines the PVCs to be the archive PVCs for SMs in the
        # supplied database.
        dbaasDatabaseArchive:
          # The name of the database.
          database: string
          # The name of the organization.
          organization: string
          # The name of the project.
          project: string
```

## Extended example

```yaml
# Standard Kubernetes API Version declaration.
apiVersion: cp.nuodb.com/v1beta1
# Standard Kubernetes Kind declaration.
kind: PersistentVolumeRebinding
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-persistentvolumerebinding
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the PersistentVolumeRebinding.
spec:
  # The rebindings to perform.
  rebindings:
  -
    # If specified, rebinds a PVC in the source namespace to a PVC in the
    # target namespace. The source namespace is the namespace of the
    # PersistentVolumeRebinding resource, while the target namespace is the
    # namespace that the controller reconciling the
    # PersistentVolumeRebinding resource is running in.
    direct:
      # The name of the existing PVC in the source namespace.
      sourceClaim: string
      # The name of the PVC to create in the target namespace.
      targetClaim: string
    # If specified, rebinds of a set of PVCs in the source namespace to a
    # set of PVCs in the target namespace. The source namespace is the
    # namespace of the PersistentVolumeRebinding resource, while the target
    # namespace is the namespace that the controller reconciling the
    # PersistentVolumeRebinding resource is running in.
    template:
      # The definition of a set of PVCs in the source namespace.
      sourceClaim:
        # If specified, defines the PVCs to be the archive PVCs for SMs in the
        # supplied database.
        dbaasDatabaseArchive:
          # The name of the database.
          database: string
          # The name of the organization.
          organization: string
          # The name of the project.
          project: string
        # If specified, defines the PVCs to be the journal PVCs for SMs in the
        # supplied database.
        dbaasDatabaseJournal:
          # The name of the database.
          database: string
          # The name of the organization.
          organization: string
          # The name of the project.
          project: string
        # If specified, defines the PVCs to have the supplied prefix with
        # ordinal suffixes.
        prefix: string
      # The definition of a set of PVCs in the target namespace.
      targetClaim:
        # If specified, defines the PVCs to be the archive PVCs for SMs in the
        # supplied database.
        dbaasDatabaseArchive:
          # The name of the database.
          database: string
          # The name of the organization.
          organization: string
          # The name of the project.
          project: string
        # If specified, defines the PVCs to be the journal PVCs for SMs in the
        # supplied database.
        dbaasDatabaseJournal:
          # The name of the database.
          database: string
          # The name of the organization.
          organization: string
          # The name of the project.
          project: string
        # If specified, defines the PVCs to have the supplied prefix with
        # ordinal suffixes.
        prefix: string
  # Labels to specify on target PVC resources created by this
  # PersistentVolumeRebinding resource.
  targetClaimLabels:
    {}
# Current observed status of the PersistentVolumeRebinding.
status:
  # List of conditions describing the state of the resource.
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
  # The status of the requested rebindings.
  rebindings:
  -
    # A human-readable message that describes the status.
    message: string
    # The name of the cluster-scoped PersistentVolume resource being rebound.
    persistentVolume: string
    # The name of the existing PVC in the source namespace.
    sourceClaim: string
    # The status of the rebinding.
    # 
    # - `Pending` indicates that the rebinding has not been initiated.
    # - `InProgress` indicates that the rebinding has been initiated but has not completed.
    # - `Succeeded` indicates that the rebinding has succeeded.
    # - `Failed` indicates that rebinding failed due to some error.
    # - `RevertInProgress` indicates that reverting of the rebinding to the source claim has been initiated, which is done when finalizing deletion of a PersistentVolumeRebinding resource.
    # - `RevertSucceeded` indicates that reverting of the rebinding to the source claim has succeeded.
    # - `RevertFailed` indicates that reverting of the rebinding to the source claim failed due to some error.
    status: string
    # The name of the PVC to create in the target namespace.
    targetClaim: string
```
