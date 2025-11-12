---
title: "CanaryRolloutTemplate"
description: "A sample CanaryRolloutTemplate object with fields documented"
summary: ""
draft: false
weight: 951
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
kind: CanaryRolloutTemplate
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-canaryrollouttemplate
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the CanaryRolloutTemplate.
spec:
  # Canary rollout steps for this template.
  steps:
  -
```

## Extended example

```yaml
# Standard Kubernetes API Version declaration.
apiVersion: cp.nuodb.com/v1beta1
# Standard Kubernetes Kind declaration.
kind: CanaryRolloutTemplate
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-canaryrollouttemplate
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the CanaryRolloutTemplate.
spec:
  # Analysis performed after every promotion step.
  analysis:
  -
    # Check for a certain status condition.
    checkStatusCondition:
      # The required condition status.
      status: True
      # A timeout after which an analysis is declared as failed.
      timeout: 1d
      # The condition type to perform analysis on.
      type: string
    # Optional deadline in seconds for executing this analaysis. Analysis runs
    # that exceed the specified deadline are interrupted and retried later.
    # Defaults to 60s.
    executionDeadlineSeconds: 1
    # Interval in which the analysis is run. Defaults to 60s.
    interval: 1d
    # The analysis name.
    name: string
    # Run the analysis on disabled targets. By default the analysis is skipped
    # on disabled resources.
    runOnDisabled: true
  # Skip disabled target resources. By default a change is promoted to all
  # matching resources.
  skipDisabled: true
  # Canary rollout steps for this template.
  steps:
  -
    # Run analysis.
    analysis:
      # Check for a certain status condition.
      checkStatusCondition:
        # The required condition status.
        status: True
        # A timeout after which an analysis is declared as failed.
        timeout: 1d
        # The condition type to perform analysis on.
        type: string
      # Optional deadline in seconds for executing this analaysis. Analysis runs
      # that exceed the specified deadline are interrupted and retried later.
      # Defaults to 60s.
      executionDeadlineSeconds: 1
      # Interval in which the analysis is run. Defaults to 60s.
      interval: 1d
      # The analysis name.
      name: string
      # Run the analysis on disabled targets. By default the analysis is skipped
      # on disabled resources.
      runOnDisabled: true
    # Pause the rollout.
    pause:
      # The duration for which the rollout is paused. Zero duration means wait
      # until manually approved.
      duration: 1d
    # Promote the change to group of targets.
    promoteTo:
      # A label query over resources to which promotion is performed. It must
      # match the resource labels. The label selector requirements are ANDed with
      # those defined in the canary rollout selector.
      labelSelector:
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
      # Limit the promotion to certain number of the matching resources. The
      # supplied limit is cumulative across promote steps (i.e. total number of
      # targets to be promoted).
      limitCount: 1
      # Limit the promotion to certain percentage of the matching resources. The
      # supplied limit is cumulative across promote steps (i.e. total percentage
      # of targets to be promoted).
      limitPercentage: 1
      # Actions performed on failed analysis. No automatic rollback is performed
      # by default.
      rollback:
        # Specifies the number of retries before giving up on rollback. Defaults to 20.
        backoffLimit: 20
        # The rollback strategy.
        strategy: Failed
# Current observed status of the CanaryRolloutTemplate.
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
```
