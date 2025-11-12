---
title: "HelmFeature"
description: "A sample HelmFeature object with fields documented"
summary: ""
draft: false
weight: 958
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
kind: HelmFeature
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-helmfeature
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the HelmFeature.
spec:
```

## Extended example

```yaml
# Standard Kubernetes API Version declaration.
apiVersion: cp.nuodb.com/v1beta1
# Standard Kubernetes Kind declaration.
kind: HelmFeature
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-helmfeature
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the HelmFeature.
spec:
  # The Helm chart version compatibility constraint for the Helm feature.
  chartCompatibility: string
  # Whether the Helm feature is optional and does not emit an error
  # if the Helm chart or product version is incompatible.
  optional: true
  # The parameter definitions referenced in values. For example, parameter
  # named `foo` is referenced using `<< .meta.params.foo >>` template.
  parameters:
    {}
  # The NuoDB product version compatibility constraint for the
  # Helm feature.
  productCompatibility: string
  # The Helm values that enable the feature.
  values:
    {}
# Current observed status of the HelmFeature.
status:
  # Revision history of Helm feature's desired state.
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
