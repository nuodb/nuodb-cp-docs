---
title: "DatabaseQuota"
description: "A sample DatabaseQuota object with fields documented"
summary: ""
draft: false
weight: 954
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
kind: DatabaseQuota
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-databasequota
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the DatabaseQuota.
spec:
  # The set of desired hard limits for each named resource.
  hard:
    {}
```

## Extended example

```yaml
# Standard Kubernetes API Version declaration.
apiVersion: cp.nuodb.com/v1beta1
# Standard Kubernetes Kind declaration.
kind: DatabaseQuota
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-databasequota
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the DatabaseQuota.
spec:
  # The set of desired hard limits for each named resource.
  hard:
    {}
  # The scope to which the quota resource limits are applied. This
  # enables defining out of band quota configuration on database
  # resources filtered and grouped by the supplied criteria.
  scope:
    # A field query over resources for which the quota is applied. It must
    # match the resource fields. Supported fields are "spec.type.sla" and
    # "spec.type.tierRef.name". More info:
    # https://kubernetes.io/docs/concepts/overview/working-with-objects/field-selectors/
    fieldSelector:
      # The list of field selector requirements, which are composed with `AND`.
      matchExpressions:
      -
        # The path of the field to apply the selector requirement to.
        key: string
        # The operator to apply to the field value. One of `=`, `==`, and `!=`.
        operator: string
        # The value to compare to.
        value: string
      # The field selector requirements as a map where each key-value pair is
      # equivalent to an element of `matchExpressions` with `operator` set to
      # `==`. The requirements are composed with `AND`.
      matchFields:
        {}
    # The label keys on which the selected databases are divided into
    # groups.
    groupByLabels:
    - string
    # A label query over resources for which the quota is applied. It must
    # match the resource labels. More info:
    # https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors
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
# Current observed status of the DatabaseQuota.
status:
  # The information about objects on which this quota has been enforced.
  # It is cleared by the quota controller after a successful
  # reconciliation.
  lastEnforced:
  -
    # Timestamp is a timestamp representing the server time when this quota was
    # enforced on a selected object.
    enforceTimestamp: 2025-11-11T21:30:40.971508Z
    # The generation that the object had at the time of quota enforcement.
    objectGeneration: 1
    # ObjectRef is a reference to the object on which this quota was enforced.
    objectRef:
      # APIGroup is the group for the resource being referenced.
      apiGroup: string
      # Kind is the type of resource being referenced.
      kind: string
      # Name is the name of resource being referenced
      name: object
  # The last observed generation.
  observedGeneration: 1
  # The current observed total usage of the named resources per scoped
  # group.
  used:
    {}
```
