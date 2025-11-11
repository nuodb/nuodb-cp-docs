---
title: "DatabaseBackup"
description: "A sample DatabaseBackup object with fields documented"
summary: ""
draft: false
weight: 953
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
apiVersion: cp.nuodb.com/v1
# Standard Kubernetes Kind declaration.
kind: DatabaseBackup
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-databasebackup
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the DatabaseBackup.
spec:
  # Source holds information about the actual backup. This field is immutable
  # after creation.
  source:
```

## Extended example

```yaml
# Standard Kubernetes API Version declaration.
apiVersion: cp.nuodb.com/v1
# Standard Kubernetes Kind declaration.
kind: DatabaseBackup
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-databasebackup
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the DatabaseBackup.
spec:
  # PluginName is the backup plugin name managing this database backup. Empty
  # value means that this backup will be executed by the default backup
  # plugin if one is configured.
  pluginName: string
  # Source holds information about the actual backup. This field is immutable
  # after creation.
  source:
    # A reference to a pre-existing backup managed by a backup plugin. This
    # field should be set if the backup already exists and only needs a
    # representation in Kubernetes. This field is immutable after creation.
    backupRef:
      # BackupHandle is the unique `backup_id` returned by the backup plugin's
      # `CreateBackup` gRPC call to refer to the backup on all subsequent calls.
      backupHandle: string
      # Plugin is the name of the backup plugin managing this backup.
      plugin: string
    # A reference to the Database object from which a backup should be created.
    # This database is assumed to be in the same namespace as the
    # DatabaseBackup object. This field should be set if the backup does not
    # exists, and needs to be created. This field is immutable after creation.
    databaseRef:
      # Name of the referent
      name: database
# Current observed status of the DatabaseBackup.
status:
  # BackupHandle is the "backup_id" value returned from the "CreateBackup"
  # gRPC call.
  backupHandle: string
  # Conditions holds the conditions for the DatabaseBackup.
  conditions:
  -
    # lastTransitionTime is the last time the condition transitioned from one status to another.
    # This should be when the underlying condition changed.  If that is not known, then using the time when the API field changed is acceptable.
    lastTransitionTime: 2025-11-11T21:30:40.971508Z
    # message is a human readable message indicating details about the transition.
    # This may be an empty string.
    message: string
    # observedGeneration represents the .metadata.generation that the condition was set based upon.
    # For instance, if .metadata.generation is currently 12, but the .status.conditions[x].observedGeneration is 9, the condition is out of date
    # with respect to the current state of the instance.
    observedGeneration: 1
    # reason contains a programmatic identifier indicating the reason for the condition's last transition.
    # Producers of specific condition types may define expected values and meanings for this field,
    # and whether the values are considered a guaranteed API.
    # The value should be a CamelCase string.
    # This field may not be empty.
    reason: string
    # status of the condition, one of True, False, Unknown.
    status: True
    # type of condition in CamelCase or in foo.example.com/CamelCase.
    type: string
  # The timestamp when the backup is taken by the underlying backup plugin.
  # This field will be filled in by the backup controller with the
  # "creation_time" value returned from "CreateBackup" gRPC call.
  creationTime: 2025-11-11T21:30:40.971508Z
```
