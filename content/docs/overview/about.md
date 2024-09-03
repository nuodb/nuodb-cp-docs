---
title: "About NuoDB Control Plane"
description: ""
summary: ""
date: 2024-08-14T13:52:09+03:00
lastmod: 2024-08-14T13:52:09+03:00
draft: false
weight: 15
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

NuoDB Control Plane (CP) enables customers to consume NuoDB in a Database as a Service (DBaaS) model.
It runs inside a Kubernetes cluster and handles provisioning and management of multiple domains, and their databases, in the _same_ cluster.
NuoDB databases are created on-demand remotely using REST services by exposing various predefined configuration options.

## Run on the Cloud

{{< card-grid >}}
{{< link-card title="Install NuoDB Control Plane" href="/docs/getting-started/deploy-nuodb-control-plane/" icon="outline/stack-push" description="Start managing NuoDB databases deployed in Kubernetes" >}}
{{< link-card title="Deploy NuoDB databases" href="/docs/getting-started/create-your-first-database/" icon="outline/rocket" description="Create NuoDB databases on-demand easily" >}}
{{< link-card title="Start Developing" href="/docs/getting-started/connect-to-the-database/" icon="outline/code" description="Connect to your database and start developing with NuoDB" >}}
{{< /card-grid >}}

## Architecture

The NuoDB Control Plane allows the creation of:

- One or more organizations
- Each organization can have one or more projects.
Each project corresponds to a NuoDB
domain with its own set of NuoDB Admin processes (APs).
- Within a project you can deploy one or more databases.
When a project is created a new or existing organization must be specified.

NuoDB CP consists of multiple modules that can be deployed independently as part of a microservices-style architecture.
Each module implements certain aspects of managing domains and databases on behalf of customers.
The following components are available to support DBaaS using this approach:

- A DBaaS REST Service that exposes multi-tenant access to external customers according to access control rules.
- A DBaaS Operator that is responsible for enforcing the desired state for databases and domains.

NuoDB domain and database are modeled as Kubernetes [Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#custom-resources) (CRs). Their [Custom Resource Definitions](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#customresourcedefinitions) (CRDs) act as contracts between NuoDB Operator and the other components.

{{< picture src="overview.png" alt="NuoDB Control Plane overview" >}}

## Key concepts

The NuoDB Control Plane can be broken down into several communicating layers.

{{< picture src="cp-arch-layers.png" alt="NuoDB Control Plane logical architecture" >}}

### REST Service

DBaaS REST Service allows multi-tenant access to external customers according to access control rules.
It exposes a REST API to external customers that enables remote management of NuoDB domains and databases using coarse-grained CRUD operations (Create, Read, Update, and Delete).
The data model used by the DBaaS REST Service to define user access control and pricing is summarized below:

- _Organizations_ have several users and payment information associated with them.
- _Projects_ are logical groupings of databases and have a service tier associated with them.
- _Users_ have roles that control access to projects and databases.

Projects abstract the aspects of domains that are relevant for DBaaS users, specifically, pricing of databases and isolation between databases. Databases within the same project will inherit the service tier from the project in which they belong, and databases in different projects will be part of different domains.

The REST APIs for projects and databases internally manipulate Domain and Database custom resources (CRs), respectively.
More information about the CRs is available in [Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#custom-resources).

### DBaaS Operator

A [Kubernetes Operator](https://coreos.com/operators/) which deploys NuoDB into Kubernetes cluster.
The Go Operator enables easy deployment of the NuoDB domain and database into the local Kubernetes cluster by using [NuoDB Helm Charts](https://github.com/nuodb/nuodb-helm-charts) and exposing high-level configuration to the user.

### NuoDB Helm charts

The NuoDB Control Plane uses the production-ready NuoDB _admin_ and _database_ Helm charts to deploy a domain (Admin Processes, APs) and a database (TEs and SMs) respectively.

### Kubernetes

Ultimately everything runs in a Kubernetes cluster - the NuoDB Control Plane itself and all APs, TEs and SMs it deploys.
Configuration information is held in _ConfigMap_ and _Secret_ resources.

### DBaaS Configuration and Offerings

Internally the NuoDB Control plane uses _Service Tiers_ and _Helm Features_ to simplify database deployment and expose various predefined configuration options available to DBaaS end users.
See [Service Tiers]({{< ref "../administration/offerings/service-tiers.md" >}}), for more information on creating re-usable configuration options.

### NuoDB

NuoDB is a distributed RDBMS that runs as a multi-process, distributed architecture running on multiple hosts, in multiple data centers.
NuoDB consisting of TE and SM processes, managed by APs.
See [NuoDB System Architecture](https://doc.nuodb.com/nuodb/latest/architecture/system-architecture/) for more information.
