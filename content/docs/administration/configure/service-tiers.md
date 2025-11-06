---
title: "Service Tiers"
description: ""
summary: ""
date: 2024-08-14T13:52:09+03:00
lastmod: 2024-08-14T13:52:09+03:00
draft: false
weight: 250
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

The NuoDB DBaaS databases are deployed using the production-ready [NuoDB Helm Charts](https://github.com/nuodb/nuodb-helm-charts) which allows fine-tuning for all aspects of database configuration.
Parameterizing the product using Helm values provides a lot of flexibility but requires in-depth knowledge of the Helm chart and the target deployment environment.
This is why with NuoDB DBaaS only a subset of configurable parameters are exposed in a controlled way.
All other parameters are defaulted by using high-level pre-configured database specifications called _service tiers_.

## Database Configuration

The NuoDB service tier is a composition of one or more Helm features.
Each feature can be referenced by multiple service tiers and contains raw Helm values that enable the feature in the Helm charts.
Both tiers and features are stored as Kubernetes [custom resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) and managed through the Kubernetes API server using standard deployment tools.

{{< callout context="note" title="Note" icon="outline/info-circle" >}}
DBaaS users themselves don’t have access to the definitions of the Helm features as they serve as an abstraction to Helm configuration.
The DBaaS administration team can define new or modify existing features and service tiers.
{{< /callout >}}

## Example: Composition

To illustrate the above, let’s have a closer look at some examples.
The sample _n1.small_ service tier references four Helm features defining different database configuration aspects.

```yaml
apiVersion: cp.nuodb.com/v1beta1
kind: ServiceTier
metadata:
  name: n1.small
  annotations:
    description: |-
      A general-purpose NuoDB service resilient to failures with 1 vCPU, 2G memory, \
      20G storage and SSD disks. The database will be started with 2 Storage Managers \
      and 3 Transaction Engines.
spec:
  features:
  - name: small-resources
  - name: small-disk
  - name: io1-disk
  - name: n1-replicas
```

The sample _n1-replicas_ feature configures the initial replicas for admin processes (AP), Transaction Engines (TE) and Storage Managers (SM) for NuoDB database.

```yaml
apiVersion: cp.nuodb.com/v1beta1
kind: HelmFeature
metadata:
  name: n1-replicas
spec:
  values:
    admin:
      replicas: 3
    database:
      sm:
        hotCopy:
          enablePod: false
        noHotCopy:
          replicas: 2
      te:
        replicas: 3
```

The below diagram shows how several Helm features (in green) are re-used and composed into different service tiers (in blue).

{{< picture src="tier-composition.jpg" alt="Service tier and Helm features composition" >}}

The feature composition is controlled by the NuoDB product version or NuoDB Helm Charts version.
In the diagram above the _thp-affinity_ feature is configured as optional by declaring `chartCompatibility` and `productCompatibility` properties which use semantic version constraints.

## Usage

Once a service tier is created, any database instance can reference it as shown below.

```yaml
apiVersion: cp.nuodb.com/v1beta1
kind: Database
metadata:
  name: acme-messaging-demo
spec:
  version: "6.0"
  type:
    tierRef:
      name: n1.small
    sla: qa
  dbName: demo
  domainRef:
    name: acme-messaging
  passwordRef:
    kind: Secret
    name: acme-messaging-demo-credentials
```

Having such flexibility for managing a discrete number of supported and exposed database configurations, empowers the DBaaS deployment, operations, and product management teams to support different deployment environments, roll out hot-fixes and enforce the desired DBaaS pricing model.
