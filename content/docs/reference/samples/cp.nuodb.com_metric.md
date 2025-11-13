---
title: "Metric"
description: "A sample Metric object with fields documented"
summary: ""
draft: false
weight: 960
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
kind: Metric
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-metric
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the Metric.
spec:
  # A list of metric descriptors.
  metrics:
  -
    # The name of the metric.
    name: string
    # Prometheus specific metric configuration.
    prometheus:
      # The Prometheus query string using Prometheus Query Language (PromQL).
      # More info: https://prometheus.io/docs/prometheus/latest/querying/basics/
      query: string
    # The units in which the metric value is reported.
    unit: string
```

## Extended example

```yaml
# Standard Kubernetes API Version declaration.
apiVersion: cp.nuodb.com/v1beta1
# Standard Kubernetes Kind declaration.
kind: Metric
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-metric
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the Metric.
spec:
  # A list of metric descriptors.
  metrics:
  -
    # A detailed description of the metric.
    description: string
    # A set of custom dimensions for classifying metric's data.
    dimensions:
    -
      # A detailed description of the metric dimension.
      description: string
      # A JSONSchema used to validate the dimension's value.
      jsonSchema: string
      # The metric dimension's name.
      name: string
    # Whether the metric is internal only or exposed to DBaaS users.
    internalOnly: true
    # The name of the metric.
    name: string
    # The NuoDB product version compatibility constraint for the metric.
    productCompatibility: string
    # Prometheus specific metric configuration.
    prometheus:
      # The Prometheus query string using Prometheus Query Language (PromQL).
      # More info: https://prometheus.io/docs/prometheus/latest/querying/basics/
      query: string
    # The units in which the metric value is reported.
    unit: string
# Current observed status of the Metric.
status:
```
