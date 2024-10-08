---
title: "On-demand backup"
description: ""
summary: ""
date: 2024-09-24T14:22:10+03:00
lastmod: 2024-09-24T14:22:10+03:00
draft: false
weight: 331
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

NuoDB DBaaS provides built-in mechanisms for database backup and clone operations leveraging volume snapshotting facilities available in the Kubernetes cluster and the corresponding storage provider.
The user configures policies for taking regular backups for databases or create on-demand backups.
Such backups are used to create a clone of the protected database in scenarios such as unexpected data corruption, data loss during a disaster, or database migrations.

## Backup contents

NuoDB database consists of one or more Storage Managers (SMs) which save the current state of the database in archive and journal volumes.
Kubernetes persistent volume claims (PVC) and persistent volumes (PV) resources are used to request and provision block storage from the underlying cloud provider.

NuoDB DBaaS database backup captures the current state of the NuoDB database including its data and configuration.
Volume snapshots are created for archive and journal volumes where the cloud provider's storage system executes, stores, and secures the snapshots.
DBaaS controls the main lifecycle of the volume snapshots (i.e. request creation and deletion) but any other lifecycle operations on snapshots must be performed using the cloud provider tools.
If multiple SMs are configured to run for redundancy in a database, there are already multiple copies of your database.
DBaaS backup facilities will choose a running SM with the lowest ordinal as a backup target.

{{< callout context="note" title="Note" icon="outline/info-circle" >}}
Table partitioning and Storage groups (TPSG) allow different SMs to serve a disjoint set of storage groups.
A complete set of database archives serving all storage groups (SGs) ensures that backup coverage is complete.
Therefore multiple SMs must be selected as backup targets when TPSG is configured.
TPSG support is not available with DBaaS yet.
{{< /callout >}}

Database configuration such as `Database` custom resource (CR) and current DBA password are stored in a backup registry.
The database configuration is used during the restore operation to validate and set default values for database volumes, and to change the DBA password.
The backup registry also containes metadata about the backup such as volume snapshot information, `PVC` resources, and backup status.

{{< callout context="note" title="Note" icon="outline/info-circle" >}}
DBaaS uses `Secret` resources as a backup registry created in the Kubernetes cluster where the backup is taken.
{{< /callout >}}

## Using on-demand backup

A backup of a running database can be initiated manually at any time.
There must be at least one _ready_ SM in the database to perform the backup operations successfully.
After being requested, the backup is executed by the system asynchronously.

### Request backup

Connect to DBaaS as described in [Connect to NuoDB Control Plane]({{< ref "../../getting-started/connect-dbaas.md" >}}).
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

The system generates a backup name with the format `yyyyMMddHHmmss` using the current time in the UTC time zone (e.g. `20241004095616`) and outputs the backup fully-qualified name.

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

### Import a backup

DBaaS uses an embedded backup manager to execute and monitor backups.
A backup registry holds a calatog about existing database backups.
By default `Secret` resources are used as a backup registry that are bound to a single Kubernetes cluster.
A DBaaS administrator can transfer a backup registry `Secret` resource from another cluster running in the same region.
For more information on backup execution and management, see [Backup Plugin]({{< ref "../../administration/backup/data-protection-overview.md#backup-plugin" >}})

Before such backup is usable in DBaaS, it must be imported by supplying its `backupHandle` and `pluginName` which manages the backup.

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
