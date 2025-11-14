---
title: "CanaryRollout"
description: "A sample CanaryRollout object with fields documented"
summary: ""
draft: false
weight: 950
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
kind: CanaryRollout
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-canaryrollout
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the CanaryRollout.
spec:
  # A strategic merge patch to apply to the metching resources. More info:
  # https://kubernetes.io/docs/tasks/manage-kubernetes-objects/update-api-object-kubectl-patch/#use-a-strategic-merge-patch-to-update-a-deployment
  patch:
    {}
  # The template reference for this rollout.
  rolloutTemplate:
    # Name of the referent
    name: string
```

## Extended example

```yaml
# Standard Kubernetes API Version declaration.
apiVersion: cp.nuodb.com/v1beta1
# Standard Kubernetes Kind declaration.
kind: CanaryRollout
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-canaryrollout
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the CanaryRollout.
spec:
  # A strategic merge patch to apply to the metching resources. More info:
  # https://kubernetes.io/docs/tasks/manage-kubernetes-objects/update-api-object-kubectl-patch/#use-a-strategic-merge-patch-to-update-a-deployment
  patch:
    {}
  # The template reference for this rollout.
  rolloutTemplate:
    # Name of the referent
    name: string
  # A label query over resources to which canary rollout applies. It must
  # match the resource labels. More info:
  # https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors
  selector:
    # matchExpressions is a list of label selector requirements. The requirements are ANDed.
    matchExpressions:
    -
      # key is the label key that the selector applies to.
      key: string
      # operator represents a key's relationship to a set of values.
      # Valid operators are In, NotIn, Exists and DoesNotExist.
      operator: string
      # values is an array of string values. If the operator is In or NotIn,
      # the values array must be non-empty. If the operator is Exists or DoesNotExist,
      # the values array must be empty. This array is replaced during a strategic
      # merge patch.
      values:
      - string
    # matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels
    # map is equivalent to an element of matchExpressions, whose key field is "key", the
    # operator is "In", and the values array contains only "value". The requirements are ANDed.
    matchLabels:
      {}
  # Specifies the number of retries before declaring a step and this canary
  # rollout as failed. Defaults to 20.
  stepBackoffLimit: 20
  # Suspended disables the canary rollout until the value is cleared. Once
  # resumed, the rollout will continue from the current step.
  suspended: true
# Current observed status of the CanaryRollout.
status:
  # Conditions holds the conditions for the canary rollout.
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
  # The number of reconciliation failure count for the current step. It is
  # reset after step completion.
  currentStepFailures: 1
  # The step index which the rollout is currently on.
  currentStepIndex: 1
  # The SHA1 checksum of rollout configuration used in the last
  # reconciliation attempt. If a checksum change is detected, the rollout is
  # restarted.
  lastObservedConfigChecksum: string
  # The step index which last promoted targets.
  lastPromotedFromIndex: 1
  # Targets to which the change is being promoted by the last promote step.
  lastPromotedTargets:
  -
    # Information about performed analysis run against the target.
    analysisRun:
    -
      # Analysis end time is the analysis completion time.
      endTime: 2025-11-11T21:30:40.971508Z
      # The human readable message indicating details about the analysis run.
      message: string
      # The name of the analysis.
      name: string
      # The result of the analysis run.
      result: Skipped
      # Analysis start time is the initial time when the analysis run was
      # performed without an error.
      startTime: 2025-11-11T21:30:40.971508Z
    # APIGroup is the group for the resource being referenced.
    apiGroup: string
    # Kind is the type of resource being referenced.
    kind: string
    # Name is the name of resource being referenced
    name: string
  # The generation observed by the controller from metadata.generation.
  observedGeneration: 1
```
