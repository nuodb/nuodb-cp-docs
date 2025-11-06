---
title: "On-demand backup"
description: ""
summary: ""
date: 2024-09-24T14:22:10+03:00
lastmod: 2024-09-24T14:22:10+03:00
draft: false
weight: 521
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---
NuoDB DBaaS (NuoDBaaS) provides built-in mechanisms for database backup and clone operations leveraging volume snapshotting facilities available in the Kubernetes cluster and the corresponding storage provider.
The user can either create database on-demand backups or configure backup policies to schedule backups and manage backup retention.
These backups are used to clone the protected database in the case of unexpected data loss, such as during a physical disaster or operational outage.

## Backup contents

A NuoDB database consists of one or more Storage Managers (SMs) that record the current database state in archive and journal volumes on disk.
Kubernetes persistent volume claims (PVC) and persistent volumes (PV) resources are used to request and provision block storage from the underlying cloud provider.

NuoDBaaS database backup captures the current state of the NuoDB database including its data and configuration.
During a backup, volume snapshots are created for the database archive and journal volumes.
The cloud provider's storage system executes, stores, and secures the underlying snapshots.
NuoDBaaS controls the lifecycle of the volume snapshots (i.e. requests creation and deletion) but any other operations on snapshots must be performed using the cloud provider tools.
If multiple SMs are configured to establish storage redundancy in a database, there are already multiple copies of your database.
In this case, NuoDBaaS backup facilities will choose a running SM with the lowest ordinal as a backup target.

{{< callout context="note" title="Table partitioning and Storage groups" icon="outline/info-circle" >}}
Table partitioning and Storage groups (TPSG) allow different SMs to serve a disjoint set of storage groups.
A complete set of database archives serving all storage groups (SGs) ensures that backup coverage is complete.
Therefore, multiple SMs must be selected as backup targets when TPSG is configured.
TPSG support is not available in NuoDBaaS yet.
{{< /callout >}}

Database configurations such as the `Database` custom resource (CR) and current DBA password are stored in the database backup catalog.
The database configuration is used during the restore operation to validate and set default values for database volumes, as well as change the DBA password.
The backup catalog also contains metadata about the backup such as volume snapshot information, `PVC` resources, and backup status.

{{< callout context="note" title="Note" icon="outline/info-circle" >}}
NuoDBaaS uses `Secret` resources as a backup catalog created in the Kubernetes cluster where the backup is taken.
{{< /callout >}}

## Using on-demand backup

A backup of a running database can be initiated manually at any time.
There must be at least one _ready_ SM in the database to perform the backup operations successfully.
After being requested, the backup is executed by the system asynchronously.

### Request backup

Connect to NuoDBaaS as described in [Connect to NuoDB Control Plane]({{< ref "../../getting-started/connect-dbaas.md" >}}).
Request on-demand backup of an existing database.

{{< tabs "create-new-backup" >}}
{{< tab "nuodb-cp" >}}

```sh
nuodb-cp backup create acme/messaging/demo
```

{{< /tab >}}
{{< tab "curl" >}}

```sh
curl -X POST -H 'Content-Type: application/json' \
 $NUODB_CP_URL_BASE/backups/acme/messaging/demo \
    -d '{}'
```

{{< /tab >}}
{{< /tabs >}}

The system generates a backup name with the format `yyyyMMddHHmmss` using the current time in the UTC zone (e.g. `20241004095616`) and outputs the backup fully-qualified name.

Example output:

{{< tabs "create-new-backup-output" >}}
{{< tab "nuodb-cp" >}}

```text
/backups/acme/messaging/demo/20241004095616
```

{{< /tab >}}
{{< tab "curl" >}}

```json
{
  "organization": "acme",
  "project": "messaging",
  "database": "demo",
  "name": "20241004095616",
  "labels": {},
  "resourceVersion": "193451345",
  "status": {
    "readyToUse": false,
    "state": "Pending",
    "retainedAs": []
 }
}
```

{{< /tab >}}
{{< /tabs >}}

### Backup state

Users can inspect the current state of a backup to ensure that backup operations are executed successfully and that the backup is usable as a restore source.

{{< callout context="caution" title="Caution" icon="outline/alert-triangle" >}}
Only backups that have `Succeeded` state can restore a database.
{{< /callout >}}

Wait for the backup to complete.

{{< tabs "wait-for-backup" >}}
{{< tab "nuodb-cp" >}}

```sh
while [ "$(nuodb-cp backup get acme/messaging/demo/20241004095616 | jq -r '.status.state')" = "Pending" ]; do
  echo "Waiting ...";
  sleep 5
done
echo "Backup completed"
```

{{< /tab >}}
{{< tab "curl" >}}

```sh
while [ "$(curl $NUODB_CP_URL_BASE/backups/acme/messaging/demo/20241004095616 | jq -r '.status.state')" = "Pending" ]; do
  echo "Waiting ...";
  sleep 5
done
echo "Backup completed"
```

{{< /tab >}}
{{< /tabs >}}

### Import backup

NuoDBaaS uses an embedded backup manager to execute and monitor backups.
A backup catalog holds information about existing database backups.
By default `Secret` resources are used as a backup catalog bound to a single Kubernetes cluster.
A NuoDBaaS administrator can transfer a backup catalog `Secret` resource from another cluster running in the same region.
For more information on backup execution and management, see [Backup Plugin]({{< ref "../../administration/backup/data-protection-overview.md#backup-plugin" >}})

Before a backup can be used in NuoDBaaS, it must be imported by supplying its `backupHandle` and the `pluginName` that manages the backup.

{{< tabs "import-backup" >}}
{{< tab "nuodb-cp" >}}

```sh
nuodb-cp backup create acme/messaging/demo/20241004095616 \
 --import-source-handle backup \
 --import-source-plugin embedded.cp.nuodb.com
```

{{< /tab >}}
{{< tab "curl" >}}

```sh
curl -X PUT -H 'Content-Type: application/json' \
 $NUODB_CP_URL_BASE/backups/acme/messaging/demo/20241004095616 \
    -d '{"importSource": {"backupHandle": "backup", "backupPlugin": "embedded.cp.nuodb.com"}}'
```

{{< /tab >}}
{{< tab "terraform" >}}

```terraform
# A backup referencing an existing backup handle
resource "nuodbaas_backup" "backup" {
  organization = nuodbaas_database.db.organization
  project      = nuodbaas_database.db.project
  database     = nuodbaas_database.db.name
  name         = "20241004095616"
  import_source = {
    backup_handle = "backup"
    backup_plugin = "embedded.cp.nuodb.com"
  }
}
```

{{< /tab >}}
{{< /tabs >}}

{{< callout context="note" title="PUT vs POST method" icon="outline/info-circle" >}}
Notice that the above call uses the _PUT_ method which creates or updates a backup and allows specifying an explicit backup name and import source as opposed to the _POST_ method used when creating an on-demand backup.
{{< /callout >}}

