---
title: "ServiceTier"
description: "A sample ServiceTier object with fields documented"
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
apiVersion: cp.nuodb.com/v1
# Standard Kubernetes Kind declaration.
kind: ServiceTier
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-servicetier
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the ServiceTier.
spec:
```

## Extended example

```yaml
# Standard Kubernetes API Version declaration.
apiVersion: cp.nuodb.com/v1
# Standard Kubernetes Kind declaration.
kind: ServiceTier
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-servicetier
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the ServiceTier.
spec:
  # The list of Helm features enabled for this service tier.
  features:
  -
    # The name of the resource.
    name: string
    # The namespace of the resource. When not specified, the current
    # namespace is assumed.
    namespace: default
    # Revision of the Helm feature used by this revision of the service tier.
    revision: string
  # The service tier update strategy used by the controller to deliver
  # changes in the service tier or referenced features to domain and
  # databases.
  updateStrategy:
    # Parameters for CanaryRollout update strategy.
    canary:
      # LocalObjectReference locates the referenced object inside the same namespace
      templateRef:
        # Name of the referent
        name: template
    # The service tier update strategy type. Defaults to Immediate.
    type: CanaryRollout
# Current observed status of the ServiceTier.
status:
  # Conditions holds the conditions for the service tier.
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
  # Revision history of service tier's desired state.
  history:
    # Resource revisions.
    revisions:
    -
      # A timestamp representing the server time when this version was created.
      creationTimestamp: 2025-11-11T21:30:40.971508Z
      # A sequence number representing a specific generation of the desired
      # state stored in the revision.
      generation: 1
      # The encoded versioned resource desired state.
      spec: ZXhhbXBsZQ==
```
