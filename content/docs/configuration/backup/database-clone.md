---
title: "Cloning a database"
description: ""
summary: ""
date: 2024-09-24T14:22:10+03:00
lastmod: 2024-09-24T14:22:10+03:00
draft: false
weight: 332
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

This section describes how to restore a database from a backup by creating a new database.
This approach has an advantage over in-place restore where an existing database state is reverted back in time because the original database is not modified or deleted during the restore operation.
To restore a database, a new database (referred to as _clone_) is created from a successful backup (referred to as the restore source).

## Restore database from backup

The cloned database state is restored from the data in the backup and the supplied configuration is merged with the one stored in the backup.
NuoDBaaS automatically infers database volume sizes from the backup or validates that the supplied values satisfy the restore.
The DBA password in the database archive is changed to match the desired value of the new database by using the previous password stored in the backup.
Database restore operation fails if the supplied backup can not be restored or if the original database configuration is incompatible with the clone.

{{< callout context="tip" title="Clone vs in-place restore" icon="outline/info-circle" >}}
A cloned database lifecycle is decoupled from the original database or the backup used to create it.
NuoDBaaS does not support restore-in-place, however, the same result can be achieved by deleting the existing database and creating a new one with the same name from the desired backup.
This operation requires downtime, so make sure that it is planned.
{{< /callout >}}

### Create a database clone

Set the `restoreFrom.backup` field of the clone to the restore source.
The backup's fully-qualified name is used in the form of `<org>/<proj>/<db>/<backup>` as a restore source.
If some prefix is omitted, it is taken from the clone database.
For example, when creating a cloned database `acme/messaging/clone` with backup source `demo/20241004095616`, the system will assume that the backup exists in organization `acme` and project `messaging`.
The cloned database can be created in any organization or project that the user has access.
The user creating the clone must have read permission to the backup used as a restore source.

{{< callout context="caution" title="Caution" icon="outline/alert-triangle" >}}
Using a backup to restore a database in a different cloud region is not supported.
{{< /callout >}}

Create a new database clone and supply the backup to restore it from.
In this example, a database named `clone` is created in the same organization and project as the original one.

{{< tabs "create-clone" >}}
{{< tab "nuodb-cp" >}}

```sh
nuodb-cp database create acme/messaging/clone \
 --restore-from-backup demo/20241004095616 \
  --dba-password changeIt
```

{{< /tab >}}
{{< tab "curl" >}}

```sh
curl -X PUT -H 'Content-Type: application/json' \
 $NUODB_CP_URL_BASE/databases/acme/messaging/clone \
    -d '{"dbaPassword": "changeIt", "restoreFrom": {"backup": "demo/20241004095616"}}'
```

{{< /tab >}}
{{< tab "terraform" >}}

```terraform
resource "nuodbaas_database" "db" {
 organization = nuodbaas_project.proj.organization
 project      = nuodbaas_project.proj.name
 name         = "clone"
 dba_password = "changeIt"
 restore_from = {
   backup = "acme/messaging/demo/20241004095616"
 }
}
```

{{< /tab >}}
{{< /tabs >}}

### Restore operation

A database restore operation is performed asynchronously.
The following prerequisites are enforced by the system:

- The backup used as a restore source must exist in the Kubernetes cluster along with the corresponding snapshots on the cloud provider's storage system
- The snapshots must be in a state that allows new volumes to be created.
Most storage providers allow changing the snapshot storage tier to achieve lower costs but with minimum archival and longer data retrieval times.
- The backup must be in `Succeeded` state
- Archive and journal volume sizes of the clone must be greater than or equal to the values of the original one
- If the original database was configured with an external journal, the clone must also have an external journal
- The NuoDB product version of the database clone must be greater than or equal to the product version of the original database

{{< callout context="note" title="Note" icon="outline/info-circle" >}}
A new database that is being restored from a backup has `Restoring` state.
{{< /callout >}}

After the database is `Available`, the DBA password stored in the restored archive is replaced with the newly supplied password.
This happens immediately after the database is ready to accept SQL connections, however, it may take several seconds before you can connect to the database.

### Troubleshooting restore failures

Any failures during the restore operation will prevent the database from starting.
The `status.message` field provides more information about the failure.

#### Missing snapshot

The restore fails because some of the snapshots are not found on the cloud provider's storage system.

```text
failed to restore backup acme-messaging-demo-20241008094059:
 snapshots not imported after 65ms: volume snapshot nuodb-cp-system/archive-volume-sm-acme-messaging-demo-zfb77wc-0-acme-messaging-demo-20241008094059-c8b8b48 failed:
 Failed to check and update snapshot content:
 failed to list snapshot for content snapcontent-archive-volume-sm-acme-messaging-demo-zfb77wc-0-acme-messaging-demo-20241008094059-c8b8b48-snap-0909778ab5d3fb463-44cz4d7: rpc error: code = Internal desc = Could not get snapshot ID "snap-0909778ab5d3fb463":
 InvalidSnapshot.NotFound: The snapshot 'snap-0909778ab5d3fb463' does not exist.
 status code: 400, request id: 768cc232-23a6-44ce-a1ac-a4f583c796c3
```

{{< details "Action" >}}
Verify that snapshot `snap-0909778ab5d3fb463` exists in the same region where DBaaS is running and the CSI driver has permission to access it.
{{< /details >}}

#### Incorrect volume size

The restore fails because the supplied archive volume size is smaller than the one in the backup.

```text
failed to restore database data:
 failed to use snapshot \"nuodb-cp-system/archive-volume-sm-acme-messaging-demo-zfb77wc-0-acme-messaging-demo-20240901000000-cz9v2zv\" for archive volume:
 configured storage size 2Gi is less than restored data size 5Gi
```

{{< details "Action" >}}
Use a larger archive volume size when creating the clone or let the system set it automatically from the backup.
{{< /details >}}

#### External journal enabled

The restore fails because the external journal is enabled on the clone but not on the original database.

```text
failed to restore database data: no snapshot for the journal volume found in backup
```

{{< details "Action" >}}
Disable external journal on the new database.
If you want to change this setting, SQL dump must be used to restore the data into a new database with an external journal enabled.
{{< /details >}}

{{< callout context="caution" title="Caution" icon="outline/alert-triangle" >}}
The external journal will be automatically enabled on the clone if it was previously enabled on the original database.
{{< /callout >}}


#### Database does not start

The database state is reported as `Restoring` but the processes can not start on the restored data.

```text
unhealthy components: [storageManagers transactionEngines];
 unhealthy resources: [deployment/te-acme-messaging-clone-dw7w9w7 statefulset/sm-acme-messaging-clone-dw7w9w7]
```

{{< details "Action" >}}
Ensure that a recent NuoDB version is configured on the clone and contact NuoDB support.
{{< /details >}}
