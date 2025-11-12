---
title: "MetricSource"
description: "A sample MetricSource object with fields documented"
summary: ""
draft: false
weight: 961
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
kind: MetricSource
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-metricsource
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the MetricSource.
spec:
  # Metric source provider configuration.
  provider:
    # Configuration for Prometheus server metrics provider.
    prometheus:
      # The HTTP URL of the Prometheus server.
      address: string
```

## Extended example

```yaml
# Standard Kubernetes API Version declaration.
apiVersion: cp.nuodb.com/v1beta1
# Standard Kubernetes Kind declaration.
kind: MetricSource
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-metricsource
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the MetricSource.
spec:
  # A label query over metric resources for which the metric source applies.
  # It must match the resource labels. If not specified, matches all metric
  # resources in the same namespace. More info:
  # https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors
  metricSelector:
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
  # Metric source provider configuration.
  provider:
    # Configuration for Prometheus server metrics provider.
    prometheus:
      # The HTTP URL of the Prometheus server.
      address: string
      # The authentication method used when communicating with Prometheus
      # server's query APIs.
      authentication:
        # The basic authentication configuration.
        basic:
          # The key in the Secret that provides the password.
          passwordKey: password
          # The secret resource reference holding the authentication information.
          secretRef:
            # Name of the referent
            name: secret
          # The key in the Secret that provides the username.
          usernameKey: user
      # Optional HTTP headers to use in the request.
      headers:
      -
        # The HTTP header key.
        key: string
        # The HTTP header value.
        value: string
      # Skip TLS hostname verification.
      insecureSkipVerify: true
      # The duration in seconds within which a prometheus query should complete.
      timeoutSec: 1
  # A label query over target resources for which the metric source applies.
  # It must match the resource labels. If not specified, matches all targets
  # in the same namespace. More info:
  # https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors
  targetsSelector:
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
# Current observed status of the MetricSource.
status:
```
