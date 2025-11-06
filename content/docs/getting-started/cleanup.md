---
title: "Remove resources"
description: ""
summary: ""
date: 2024-08-14T13:44:13+03:00
lastmod: 2024-08-14T13:44:13+03:00
draft: false
weight: 150
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

Once you are done with the database, do not forget to remove the provisioned NuoDB resources.

## Delete database

{{< callout context="danger" title="Danger" icon="outline/alert-octagon" >}}
Deleting NuoDB database will delete all persistent storage associated with it along with any user data stored in the database.
{{< /callout >}}

{{< tabs "delete-database" >}}
{{< tab "nuodb-cp" >}}

```sh
nuodb-cp database delete acme/messaging/demo
```

{{< /tab >}}
{{< tab "curl" >}}

```sh
curl -X DELETE $NUODB_CP_URL_BASE/databases/acme/messaging/demo
```

{{< /tab >}}
{{< /tabs >}}

## Delete project

{{< tabs "delete-project" >}}
{{< tab "nuodb-cp" >}}

```sh
nuodb-cp project delete acme/messaging
```

{{< /tab >}}
{{< tab "curl" >}}

```sh
curl -X DELETE $NUODB_CP_URL_BASE/projects/acme/messaging
```

{{< /tab >}}
{{< /tabs >}}

## Uninstall NuoDB Control Plane

This section describes how to uninstall NuoDB Control Plane from the Kubernetes cluster.

### Delete custom resources

Delete all custom resources (CR) that have been created in `nuodb-cp-system` namespace.
For some of the CRs, DBaaS operator performs cleanup actions and removes [finalizers](https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/) before they are deleted from Kubernetes API server.

```sh
kubectl config set-context --current --namespace=nuodb-cp-system
for crd in $(kubectl get customresourcedefinitions --no-headers -o custom-columns=":metadata.name" | grep ".cp.nuodb.com"); do
    kubectl get $crd -o name | xargs -r kubectl delete --wait=false
done
for crd in $(kubectl get customresourcedefinitions --no-headers -o custom-columns=":metadata.name" | grep ".cp.nuodb.com"); do
    kubectl get $crd -o name | xargs -r kubectl delete
done
kubectl get secrets -o name --selector=cp.nuodb.com/organization | xargs -r kubectl delete
kubectl get pvc -o name --selector=group=nuodb | xargs -r kubectl delete
```

### Uninstall DBaaS components

Uninstall all Helm charts following the order below.

```sh
helm uninstall nuodb-cp-rest --namespace nuodb-cp-system
helm uninstall nuodb-cp-operator --namespace nuodb-cp-system
helm uninstall nuodb-cp-crd --namespace nuodb-cp-system
helm uninstall ingress-nginx --namespace nginx
helm uninstall cert-manager --namespace cert-manager
```

Delete the provisioned namespaces.

```sh
kubectl delete namespace nuodb-cp-system
kubectl delete namespace cert-manager
kubectl delete namespace nginx
```
