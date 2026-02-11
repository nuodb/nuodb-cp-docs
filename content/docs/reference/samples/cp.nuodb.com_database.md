---
title: "Database"
description: "A sample Database object with fields documented"
summary: ""
draft: false
weight: 955
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
kind: Database
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-database
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the Database.
spec:
  # The name use for this database
  dbName: demo
  # Reference pointing to the name of the NuoDB domain associated with this
  # database instance
  domainRef:
    # Name of the referent
    name: domain
  # Reference pointing to the name of the Secret holding the DBA password
  passwordRef:
    # Kind of the values referent, valid values are ('Secret', 'ConfigMap').
    kind: Secret
    # Name of the values referent. Should reside in the same namespace as the
    # referring resource.
    name: password
  # Database instance service type
  type:
    # The service instance SLA type
    sla: prod
    # The service instance tier type
    tierRef:
      # The name of the resource.
      name: tier
  # NuoDB image version used for the database
  version: 7.0.2
```

## Extended example

```yaml
# Standard Kubernetes API Version declaration.
apiVersion: cp.nuodb.com/v1beta1
# Standard Kubernetes Kind declaration.
kind: Database
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-database
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the Database.
spec:
  # ArchiveVolume configures the database archive volume.
  archiveVolume:
    # Resize the volume automatically when a threshold is reached. The volume
    # storage class must support volume expansion.
    automaticResize:
      # Determines the new size of the volume. By default the volume size will be
      # increased by 20%. If maxSize is set, then the new volume size will be
      # evaluated as the minimum of maxSize and result of applying the growth
      # configuration.
      growth:
        # Increase the volume size by a constant number of bytes.
        increment: 5Gi
        # Increase the volume size by a factor of the current size. Valid are
        # values between 1.01 and 9.99.
        scale: string
      # The maximum volume size.
      maxSize: 5Gi
      # The threshold at which the volume will be expanded.
      threshold:
        # Threshold in number of available bytes at which volume expansion is
        # performed.
        bytesAvailable: 5Gi
        # Threshold in percentage of available disk space at which volume expansion
        # is performed.
        percentageAvailable: 1
    # DataSourceRef specifies the object from which to populate the volume with
    # data, if a non-empty volume is desired. An existing VolumeSnapshot object
    # (snapshot.storage.k8s.io/VolumeSnapshot) or an existing PVC
    # (PersistentVolumeClaim) are supported.
    dataSourceRef:
      # APIGroup is the group for the resource being referenced.
      # If APIGroup is not specified, the specified Kind must be in the core API group.
      # For any other third-party types, APIGroup is required.
      apiGroup: string
      # Kind is the type of resource being referenced
      kind: string
      # Name is the name of resource being referenced
      name: datasource
      # Namespace is the namespace of resource being referenced
      # Note that when a namespace is specified, a gateway.networking.k8s.io/ReferenceGrant object is required in the referent namespace to allow that namespace's owner to accept the reference. See the ReferenceGrant documentation for details.
      # (Alpha) This field requires the CrossNamespaceVolumeDataSource feature gate to be enabled.
      namespace: default
    # StorageClassName is the name of the StorageClass required for this
    # volume.
    storageClassName: string
    # VolumeSize is the storage resource request, in bytes (e,g. 5Gi = 5GiB = 5
    # * 1024 * 1024 * 1024)
    volumeSize: 5Gi
  # The Helm Chart source
  chart:
    # The Helm chart name available in the remote repository.
    name: string
    # Whether to pin the Helm chart version to the latest version currently
    # available in the Helm repository so that future reconciliations doesn't
    # automatically pick up new Helm chart version. This is used only if the
    # Helm chart version is set to empty string ("") which represents the
    # user's intent to use the latest chart version.
    pinLatestVersion: true
    # A https URL to a Helm repo to download the chart from.
    repository: string
    # The version of the chart or semver constraint of the chart to find.
    version: 7.0.2
  # The name use for this database
  dbName: demo
  # Reference pointing to the name of the NuoDB domain associated with this
  # database instance
  domainRef:
    # Name of the referent
    name: domain
  # FQDN for the database endpoint
  hostname: string
  # JournalVolume configures the database external journal volume. If
  # defined, a separate volume for the database journal will be provisioned.
  journalVolume:
    # Resize the volume automatically when a threshold is reached. The volume
    # storage class must support volume expansion.
    automaticResize:
      # Determines the new size of the volume. By default the volume size will be
      # increased by 20%. If maxSize is set, then the new volume size will be
      # evaluated as the minimum of maxSize and result of applying the growth
      # configuration.
      growth:
        # Increase the volume size by a constant number of bytes.
        increment: 5Gi
        # Increase the volume size by a factor of the current size. Valid are
        # values between 1.01 and 9.99.
        scale: string
      # The maximum volume size.
      maxSize: 5Gi
      # The threshold at which the volume will be expanded.
      threshold:
        # Threshold in number of available bytes at which volume expansion is
        # performed.
        bytesAvailable: 5Gi
        # Threshold in percentage of available disk space at which volume expansion
        # is performed.
        percentageAvailable: 1
    # DataSourceRef specifies the object from which to populate the volume with
    # data, if a non-empty volume is desired. An existing VolumeSnapshot object
    # (snapshot.storage.k8s.io/VolumeSnapshot) or an existing PVC
    # (PersistentVolumeClaim) are supported.
    dataSourceRef:
      # APIGroup is the group for the resource being referenced.
      # If APIGroup is not specified, the specified Kind must be in the core API group.
      # For any other third-party types, APIGroup is required.
      apiGroup: string
      # Kind is the type of resource being referenced
      kind: string
      # Name is the name of resource being referenced
      name: datasource
      # Namespace is the namespace of resource being referenced
      # Note that when a namespace is specified, a gateway.networking.k8s.io/ReferenceGrant object is required in the referent namespace to allow that namespace's owner to accept the reference. See the ReferenceGrant documentation for details.
      # (Alpha) This field requires the CrossNamespaceVolumeDataSource feature gate to be enabled.
      namespace: default
    # StorageClassName is the name of the StorageClass required for this
    # volume.
    storageClassName: string
    # VolumeSize is the storage resource request, in bytes (e,g. 5Gi = 5GiB = 5
    # * 1024 * 1024 * 1024)
    volumeSize: 5Gi
  # The maintenance configuration for the database.
  maintenance:
    # The time at which to mark the domain or database as being disabled.
    expiresAtTime: 2025-11-11T21:30:40.971508Z
    # The time delta until the domain or database is marked as being
    # disabled. This value is used to calculate the ExpiresAtTime value
    # that is injected by the controller on creation or update.
    expiresIn: 1d
    # Whether to disable the domain or database by scaling down all
    # associated workloads to replicas=0.
    isDisabled: False
    # Whether to gracefully shutdown domain or database workloads. This
    # causes all database workloads to be shutdown before domain workload,
    # with TEs being shutdown before SMs. This has no effect if the domain
    # or database is not disabled.
    shouldShutdownGracefully: True
  # Reference pointing to the name of the Secret holding the DBA password
  passwordRef:
    # DataKey is the data key where the a specific value can be
    # found at. Defaults to "data"
    dataKey: data
    # Kind of the values referent, valid values are ('Secret', 'ConfigMap').
    kind: Secret
    # Name of the values referent. Should reside in the same namespace as the
    # referring resource.
    name: password
  # RestoreFrom indicates that the database should be restored from a
  # backup rather than having an empty state.
  restoreFrom:
    # The backoff duration in seconds after failed restore operation. The total
    # backoff interval will be multiplied by the number of failures.
    backOffSec: 30
    # A reference to the DatabaseBackup resource from which to populate the
    # database state.
    backupRef:
      # Name of the referent
      name: backup
    # The Database resource restore policy. By default, the database
    # spec will be merged with the one stored in the backup if possible.
    databaseRestorePolicy: Merge
    # Maximum number of retries that should be attempted on failure before
    # giving up. Set to zero or negative number to disable
    # retries.
    maxRetries: 20
  # Additional configuration for the Helm release
  template:
    # The backoff duration in seconds after failed helm install/upgrade. The
    # total backoff interval will be multiplied by the number of failures.
    backOffSec: 60
    # Defines what happens with the persistent volume claims after the Helm
    # release is uninstalled. Defaults to 'Delete' which means that all
    # associated PVCs are removed.
    dataRetentionPolicy: Delete
    # Maximum number of retries that should be attempted on failures before
    # giving up. Defaults to 20. Set to negative number to disable retries.
    maxRetries: 20
    # The target namespace to install the Helm release in
    namespace: default
    # The name of the Helm release
    releaseName: string
  # Database instance service type
  type:
    # The service instance SLA type
    sla: prod
    # The service instance tier type
    tierRef:
      # Features that override the service tier Helm values for this resource.
      featureOverrides:
      -
        # The name of the resource.
        name: string
        # The namespace of the resource. When not specified, the current
        # namespace is assumed.
        namespace: default
        # Revision of the Helm feature used by this revision of the service tier.
        revision: string
      # The name of the resource.
      name: tier
      # The namespace of the resource. When not specified, the current
      # namespace is assumed.
      namespace: default
      # Opaque parameters passed to the Helm features of the referenced service
      # tier.
      parameters:
        {}
      # Revision of the service tier.
      revision: string
  # NuoDB image version used for the database
  version: 7.0.2
# Current observed status of the Database.
status:
  # Components holds information about the observed status of the Database
  # components
  components:
    # Last update timestamp for this status.
    lastUpdateTime: 2025-11-11T21:30:40.971508Z
    # Storage Manager component status information.
    storageManagers:
    -
      # Group defines the schema of this representation of an object.
      group: string
      # Kind is a string value representing the REST resource this object represents.
      kind: string
      # A human readable message indicating details about why the resource is in
      # this condition
      message: string
      # Name is the resource
      name: string
      # ReadyReplicas is the number of pods created for this resource with a
      # Ready Condition.
      readyReplicas: 1
      # Replicas is the number of pods created by the resource controller.
      replicas: 1
      # The state of the resource
      state: string
      # Version defines the schema version of this representation of an object.
      version: 7.0.2
    # Transaction Engine component status information.
    transactionEngines:
    -
      # Group defines the schema of this representation of an object.
      group: string
      # Kind is a string value representing the REST resource this object represents.
      kind: string
      # A human readable message indicating details about why the resource is in
      # this condition
      message: string
      # Name is the resource
      name: string
      # ReadyReplicas is the number of pods created for this resource with a
      # Ready Condition.
      readyReplicas: 1
      # Replicas is the number of pods created by the resource controller.
      replicas: 1
      # The state of the resource
      state: string
      # Version defines the schema version of this representation of an object.
      version: 7.0.2
  # Conditions holds the conditions for the Database.
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
  # The backup handle that was used to restore this database.
  lastRestoredBackupHandle: string
  # The last observed generation.
  observedGeneration: 1
  # ReleaseRefs contain references to the dependant HelmApp resources that
  # have this object as an owner. Expected to be non-empty once the
  # corresponding applications are installed.
  releaseRefs:
  -
    # APIGroup is the group for the resource being referenced.
    apiGroup: string
    # Kind is the type of resource being referenced.
    kind: string
    # The revision of the last successful Helm release.
    lastReleaseRevision: 1
    # Name is the name of resource being referenced
    name: string
    # The name of the Helm release.
    releaseName: string
    # The target namespace of the Helm release.
    releaseNamespace: string
    # Whether the Helm release has been synchronized.
    synced: true
  # The number of failed database restore attempts. It is reset after a
  # successful database restore
  restoreFailures: 1
  # The observed NuoDB image version used for the domain.
  version: 7.0.2
```
