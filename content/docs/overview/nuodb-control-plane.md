---
title: "NuoDB Control Plane"
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


The NuoDB Control Plane (CP) empowers customers to leverage NuoDB in a Database as a Service (DBaaS) model.
Operating within a Kubernetes cluster, it manages the provisioning and administration of multiple administrative domains and their databases, all within the same cluster.
NuoDB databases are dynamically created remotely with a variety of predefined configuration options available.

## Run on the Cloud

{{< card-grid >}}
{{< link-card title="Install NuoDB Control Plane" href="../getting-started/installation.md" icon="outline/stack-push" description="Start managing NuoDB databases deployed in Kubernetes" >}}
{{< link-card title="Deploy NuoDB databases" href="../getting-started/create-database.md" icon="outline/rocket" description="Create NuoDB databases on-demand easily" >}}
{{< link-card title="Start Developing" href="../getting-started/connect-database.md" icon="outline/code" description="Connect to your database and start developing with NuoDB" >}}
{{< /card-grid >}}

## Architecture

The NuoDB Control Plane allows the creation of:

- One or more organizations
- Each organization can have one or more projects.
Each project corresponds to a NuoDB
domain with its own set of NuoDB Admin processes (APs).
- Within a project, one or more databases can be deployed.
When a project is created a new or existing organization must be specified.

NuoDB CP is composed of several modules that can be independently deployed as part of a microservices-style architecture.
Each module is responsible for managing specific aspects of domains and databases on behalf of customers.
The following components are available to support DBaaS using this approach:

- A DBaaS REST Service that exposes multi-tenant access to external customers according to access control rules.
- A DBaaS Operator that is responsible for enforcing the desired state for databases and domains.

NuoDB domain and database are modeled as Kubernetes [Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#custom-resources) (CRs). Their [Custom Resource Definitions](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#customresourcedefinitions) (CRDs) act as contracts between NuoDB Operator and the other components.

{{< picture src="overview.png" alt="NuoDB Control Plane overview" >}}

## Key concepts

The NuoDB Control Plane can be broken down into several communicating layers.

{{< picture src="cp-arch-layers.png" alt="NuoDB Control Plane logical architecture" >}}

### REST Service

DBaaS REST Service facilitates multi-tenant access for external customers in accordance with access control rules.
It exposes a REST API, enabling remote management of NuoDB domains and databases through coarse-grained CRUD operations (Create, Read, Update, and Delete).
The data model used by the DBaaS REST Service to define user access control is outlined below:

- _Organizations_ consist of several users and policies.
- _Projects_ serve as logical groupings of databases and have a service tier associated with them.
- _Users_ are assigned roles that dictate access to projects and databases.

Projects abstract the relevant aspects of domains for DBaaS users and provide isolation between databases.
Databases within the same project will inherit the service tier from the project they belong to, while databases in different projects will be managed in separate domains.

The REST APIs for projects and databases internally manipulate Domain and Database custom resources (CRs), respectively.

### DBaaS Operator

The DBaaS Operator is a [Kubernetes Operator](https://coreos.com/operators/) which deploys NuoDB into the Kubernetes cluster.
The Operator simplifies the process of deploying the NuoDB domain and database into the local Kubernetes cluster by utilizing [NuoDB Helm Charts](https://github.com/nuodb/nuodb-helm-charts) and exposing high-level configuration options to the user.

### NuoDB Helm charts

The NuoDB Control Plane uses the production-ready NuoDB _admin_ and _database_ Helm charts to deploy a domain (NuoDB Admin processes, APs) and a database (Transaction Engines, TEs and Storage Managers, SMs) respectively.

### Kubernetes

Ultimately, the entire NuoDB DBaaS system operates within a Kubernetes cluster, including the NuoDB Control Plane and all APs, TEs, and SMs it deploys.
Configuration information is stored in _ConfigMap_ and _Secret_ resources.

### DBaaS Configuration and Offerings

Internally, the NuoDB Control Plane leverages _Service Tiers_ and _Helm Features_ to streamline database deployment and provide DBaaS end users with a variety of predefined configuration options.
For more information on creating reusable configuration options, refer to the documentation on [Service Tiers]({{< ref "../administration/offerings/service-tiers.md" >}}).

### NuoDB

NuoDB is a distributed Relational Database Management System (RDBMS) that operates as a multi-process, distributed architecture across multiple hosts and data centers.
NuoDB is composed of TE and SM database processes, which are managed by APs.
For more information on NuoDB's system architecture, refer to the [NuoDB System Architecture](https://doc.nuodb.com/nuodb/latest/architecture/system-architecture/) documentation.
