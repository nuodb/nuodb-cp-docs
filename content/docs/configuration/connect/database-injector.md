---
title: "Database injector"
description: ""
summary: ""
date: 2024-08-14T14:20:07+03:00
lastmod: 2024-08-14T14:20:07+03:00
draft: false
weight: 321
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

The NuoDB Control Plane (CP) is used to create NuoDB databases for applications that are running in the same [Kubernetes][1] cluster.
This document describes how to use the database injector to supply database connection information to a sample YCSB application.

## Prerequisites

- A running [Kubernetes cluster][2]
- [kubectl][3] installed and able to access the cluster.

## Installing NuoDB Control Plane

Install NuoDB CP as documented in the [Deployment]({{< ref "../../getting-started/installation.md" >}}) section.

### Enable Cluster-scoped Access

By default NuoDB operator will monitor only the local namespace for NuoDB [custom resources][4].
If cluster-scoped access is required, set the `cpOperator.watchNamespace.enabled=false` Helm value during installation. E.g.:

```sh
helm install nuodb-cp-operator nuodb-cp/nuodb-cp-operator \
    --namespace nuodb-cp-system \
    --set cpOperator.watchNamespace.enabled=false \
    --set nuodb.serviceAccount.create=false \
    --set nuodb.serviceAccount.name=default \
    ...
```

{{< callout context="note" title="Note" icon="outline/info-circle" >}}
The `nuodb` service account (SA) creation is disabled in the above command for simplicity.
To enable NuoDB Kubernetes Aware Admin (KAA) capabilities, give the NuoDB processes special permissions to access the Kubernetes API server.
For more information, please see [Automatic Management of NuoDB State](https://doc.nuodb.com/nuodb/latest/deployment-models/kubernetes-environments/kubernetes-aware-admin/).
For cluster-scoped deployments, provision the NuoDB SA and RBAC beforehand in each namespace where NuoDB databases will be created.
{{< /callout >}}

## Database Injection

NuoDB operator can inject database information into ConfigMap's _data_ once the database is ready.
This enables easy data source configuration in the application container and acts as a dependency mechanism without the need of additional _init_ containers.

Database connection details are populated _after_ the database is created and ready to accept SQL connections which blocks application container creation.
All containers that have references to the target ConfigMap will fail with `CreateContainerConfigError` due to the ConfigMap key being absent.

### Injected Properties

| Property | Description |
| ----- | ----------- |
| `dbName` | NuoDB database name |
| `dbHost` | The FQDN of the domain managing this database. If external access is enabled on the domain, the property will be populated with the external FQDN. |
| `dbPort` | The database port for SQL clients. If external access is enabled on the domain, the property will be populated with the Ingress Controller's service port (by default _443_). |
| `caPem` | The Certificate Authority (CA) certificate for the domain. Used by SQL clients that need to enable TLS encryption on the database connections. If TLS is not enabled on the domain, the property is not injected. |

### Creating Database

NuoDB domain and database resources can be created either via REST API or declaratively using [custom resources][4].
This example creates NuoDB domain and database using custom resources.

```sh
kubectl apply -f https://nuodb.github.io/nuodb-cp-docs/samples/domain.yaml
kubectl apply -f https://nuodb.github.io/nuodb-cp-docs/samples/database.yaml
```

## Creating Sample Application

Create a sample Yahoo! Cloud Serving Benchmark (YCSB) application and reference the database information into the _app_ container.

```sh
kubectl apply -f https://nuodb.github.io/nuodb-cp-docs/samples/ycsb-demo-app.yaml
```

Wait for the database to become ready.

```sh
kubectl wait --for=condition=ready database acme-messaging-demo
```

Verify that database information is injected into `acme-messaging-demo-info` ConfigMap's data and the YCSB Pod is _Running_.

```sh
kubectl get cm acme-messaging-demo-info -o yaml
kubectl get pods -l app=ycsb-load
```

### Injector Configuration

Database injection is controlled by custom annotations specified on the target ConfigMap.

| Annotation | ConfigMap data key | Description | Example Value |
| ----- | ----- | ----------- | ------ |
| `cp.nuodb.com/inject-database` | `cp.inject-database` | Specifies that the object should be injected with database information. The annotation value is a reference to a database object in form of "name" or "namespace/name". If the namespace part is omitted, it is inferred from the target ConfigMap. | `acme-messaging-demo` |
| `cp.nuodb.com/inject-database-properties` | `cp.inject-database-properties` | Specifies the database properties that should be injected into the target object. The value is a comma-delimited string of properties. By default, all connection information properties are injected. | `dbHost,dbName` |
| `cp.nuodb.com/inject-database-<property>-field` | `cp.inject-database-<property>-field` | Specifies the database property to target field mapping. By default the field name will match the property name, e.g. "dbHost" property will be injected as "dbHost" field. See [Injected Properties](#injected-properties). | `"cp.nuodb.com/inject-database-dbHost-field": "host"` |
| `cp.nuodb.com/inject-database-notready` | `cp.inject-database-notready` | Whether a non-ready database should be injected. Only the annotation existence is checked. Its value is currently not used. By default, the database is injected only after it becomes ready. | `true` |

There is an alternative way to configure database injection using the ConfigMap _data_ markers.
Their values are treated the same way as the annotation value.
This can be used in environments where custom annotations can't be specified.

## Cleanup

Delete all resources.

```sh
kubectl delete -f https://nuodb.github.io/nuodb-cp-docs/samples/ycsb-demo-app.yaml
kubectl delete -f https://nuodb.github.io/nuodb-cp-docs/samples/database.yaml
kubectl delete -f https://nuodb.github.io/nuodb-cp-docs/samples/domain.yaml
```

[1]: https://kubernetes.io/docs/home/
[2]: https://kubernetes.io/docs/concepts/overview/components/
[3]: https://kubernetes.io/docs/tasks/tools/
[4]: https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#custom-resources
