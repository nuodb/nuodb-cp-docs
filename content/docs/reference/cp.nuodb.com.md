---
title: "NuoDB CRDs Reference"
description: "Custom resource definitions (CRDs) for NuoDB Control Plane operator"
summary: ""
draft: false
weight: 912
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

## Packages
- [cp.nuodb.com/v1beta1](#cpnuodbcomv1beta1)


## cp.nuodb.com/v1beta1

Package v1beta1 contains API Schema definitions for the cp v1beta1 API group

### Resource Types
- [CanaryRollout](#canaryrollout)
- [CanaryRolloutTemplate](#canaryrollouttemplate)
- [Database](#database)
- [DatabaseBackup](#databasebackup)
- [DatabaseBackupPolicy](#databasebackuppolicy)
- [DatabaseQuota](#databasequota)
- [Domain](#domain)
- [HelmApp](#helmapp)
- [HelmFeature](#helmfeature)
- [IdentityProvider](#identityprovider)
- [Metric](#metric)
- [MetricSource](#metricsource)
- [RoleTemplate](#roletemplate)
- [ServiceTier](#servicetier)



#### AccessRuleEntry







_Appears in:_
- [RoleTemplateSpec](#roletemplatespec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `verb` _string_ | The verb to grant access to with this access rule entry, which maps<br />to HTTP request methods as follows:<br />- `read`: GET<br />- `write`: PUT, POST<br />- `delete`: DELETE<br />`all` denotes that the request method is unconstrained for this<br />access rule entry. |  | Enum: [read write delete all] <br /> |
| `resource` _string_ | The resource or set of resources to grant access to. If the value<br />begins with a slash (`/`), then the value denotes a resource path.<br />Otherwise, the value denotes a scope in the hierarchy of the DBaaS<br />resources that this access rule entry grants access to, of the form<br />`<organization>`, `<organization>/<project>`, or<br />`<organization>/<project>/<database>`. In either case, parameterized<br />path segments of the form `\{organization\}` or `\{user\}` may appear<br />that are resolved when the role template is assigned to a user. |  | Pattern: `^/?([a-z][a-z0-9]*/\|[\{][a-z][a-z0-9]*[\}]/)*([a-z][a-z0-9-]*\|[\{][a-z][a-z0-9]*[\}]\|[*])$` <br /> |
| `sla` _string_ | The SLA to constrain access to. This constraint only applies to<br />projects and resources contained within projects, such as databases<br />and backups. |  | Pattern: `^[a-z][a-z0-9]*$` <br /> |


#### AuthenticationMethod



Authentication method.



_Appears in:_
- [PrometheusMetricProvider](#prometheusmetricprovider)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `basic` _[BasicAuthenticationConfig](#basicauthenticationconfig)_ | The basic authentication configuration. |  |  |


#### BackupRetention



BackupRetention defines the GFS (Grandfather-Father-Son) backup retention
policy.



_Appears in:_
- [DatabaseBackupPolicySpec](#databasebackuppolicyspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `hourly` _integer_ | Hourly retention for backups. |  |  |
| `daily` _integer_ | Daily retention for backups. |  |  |
| `weekly` _integer_ | Weekly retention for backups. |  |  |
| `monthly` _integer_ | Monthly retention for backups. |  |  |
| `yearly` _integer_ | Yearly retention for backups. |  |  |
| `settings` _[BackupRotationSettings](#backuprotationsettings)_ | Additional backup rotation settings. |  |  |


#### BackupRotationSettings



BackupRotationSettings define additional settings to fine-tune the backup
rotation scheme.



_Appears in:_
- [BackupRetention](#backupretention)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `dayOfWeek` _integer_ | The day of the week (Sunday = 0, ...) used to promote backup to weekly .<br />Weekly can be promoted from daily from any day of the week. For example,<br />the weekly backup may be chosen to be promoted from Sunday daily backups.<br />If a successful Sunday backup is not found due to a missed run or an<br />error, it will choose the next closest, such as a Saturday backup, and<br />treat that as weekly instead. Defaults to Sunday. | 0 | Maximum: 6 <br />Minimum: 0 <br /> |
| `monthOfYear` _integer_ | The month of the year (January = 1, ...) used to promote backup to<br />yearly. Yearlies can be promoted from any month of the year, such as<br />January, December, or the company’s fiscal year-end. Defaults to January. | 1 | Maximum: 12 <br />Minimum: 1 <br /> |
| `relativeToLast` _boolean_ | Whether to apply the backup rotation scheme relative to the last<br />successful backup instead to the current time. This allows older backups<br />for the configured number of periods to be retained in case the policy is<br />suspended or latest backups are failing. Enabled by default. | true |  |
| `promoteLatestToHourly` _boolean_ | Whether to promote the latest backup within the hour if multiple backups<br />exist for that hour. By default the first successful backup from the hour<br />is retained. | false |  |
| `promoteLatestToDaily` _boolean_ | Whether to promote the latest backup within the day if multiple backups<br />exist for that day. By default the first successful backup from the day<br />is retained. | false |  |
| `promoteLatestToMonthly` _boolean_ | Whether to promote the latest backup within the month if multiple backups<br />exist for that month. By default the first successful backup from the<br />month is retained. | false |  |


#### BackupSource



BackupSource defines a pre-existing backup managed by a backup plugin.



_Appears in:_
- [DatabaseBackupSource](#databasebackupsource)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `plugin` _string_ | Plugin is the name of the backup plugin managing this backup. |  |  |
| `backupHandle` _string_ | BackupHandle is the unique `backup_id` returned by the backup plugin's<br />`CreateBackup` gRPC call to refer to the backup on all subsequent calls. |  |  |


#### BaseResourceStatus



BaseResourceStatus defines the observed state of an installed resource



_Appears in:_
- [WorkloadStatus](#workloadstatus)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `name` _string_ | Name is the resource |  |  |
| `kind` _string_ | Kind is a string value representing the REST resource this object represents. |  |  |
| `version` _string_ | Version defines the schema version of this representation of an object. |  |  |
| `group` _string_ | Group defines the schema of this representation of an object. |  |  |
| `state` _string_ | The state of the resource |  |  |
| `message` _string_ | A human readable message indicating details about why the resource is in<br />this condition |  |  |


#### BasicAuthenticationConfig



Basic authentication configuration.



_Appears in:_
- [AuthenticationMethod](#authenticationmethod)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `secretRef` _[LocalObjectReference](#localobjectreference)_ | The secret resource reference holding the authentication information. |  |  |
| `usernameKey` _string_ | The key in the Secret that provides the username. | user |  |
| `passwordKey` _string_ | The key in the Secret that provides the password. | password |  |


#### CanaryAnalysisResult

_Underlying type:_ _string_

CanaryAnalysisResult describes the result of a canary analysis run.

_Validation:_
- Enum: [Skipped Failed Succeeded Pending]

_Appears in:_
- [CanaryAnalysisRunInfo](#canaryanalysisruninfo)

| Field | Description |
| --- | --- |
| `Skipped` |  |
| `Failed` |  |
| `Succeeded` |  |
| `Pending` |  |


#### CanaryAnalysisRunInfo



CanaryAnalysisRunInfo defines information about canary analysis run.



_Appears in:_
- [CanaryRolloutTargetReference](#canaryrollouttargetreference)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `name` _string_ | The name of the analysis. |  |  |
| `result` _[CanaryAnalysisResult](#canaryanalysisresult)_ | The result of the analysis run. |  | Enum: [Skipped Failed Succeeded Pending] <br /> |
| `startTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#time-v1-meta)_ | Analysis start time is the initial time when the analysis run was<br />performed without an error. |  |  |
| `endTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#time-v1-meta)_ | Analysis end time is the analysis completion time. |  |  |
| `message` _string_ | The human readable message indicating details about the analysis run. |  |  |


#### CanaryRollout



CanaryRollout is the Schema for the canaryrollouts API.





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `cp.nuodb.com/v1beta1` | | |
| `kind` _string_ | `CanaryRollout` | | |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[CanaryRolloutSpec](#canaryrolloutspec)_ |  |  |  |


#### CanaryRolloutAnalysis



CanaryRolloutAnalysis defines the analysis run on target resources after a
changed has been roll out.



_Appears in:_
- [CanaryRolloutStep](#canaryrolloutstep)
- [CanaryRolloutTemplateSpec](#canaryrollouttemplatespec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `name` _string_ | The analysis name. |  |  |
| `interval` _[Duration](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#duration-v1-meta)_ | Interval in which the analysis is run. Defaults to 60s. |  | Pattern: `^([0-9]+(\.[0-9]+)?(ns\|us\|µs\|ms\|s\|m\|h))+$` <br />Type: string <br /> |
| `executionDeadlineSeconds` _integer_ | Optional deadline in seconds for executing this analaysis. Analysis runs<br />that exceed the specified deadline are interrupted and retried later.<br />Defaults to 60s. |  | Minimum: 1 <br /> |
| `runOnDisabled` _boolean_ | Run the analysis on disabled targets. By default the analysis is skipped<br />on disabled resources. |  |  |
| `checkStatusCondition` _[StatusConditionAnalysis](#statusconditionanalysis)_ | Check for a certain status condition. |  |  |


#### CanaryRolloutSpec



CanaryRolloutSpec defines the desired state of CanaryRollout.



_Appears in:_
- [CanaryRollout](#canaryrollout)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `selector` _[LabelSelector](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#labelselector-v1-meta)_ | A label query over resources to which canary rollout applies. It must<br />match the resource labels. More info:<br />https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors |  |  |
| `patch` _[JSON](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#json-v1-apiextensions-k8s-io)_ | A strategic merge patch to apply to the metching resources. More info:<br />https://kubernetes.io/docs/tasks/manage-kubernetes-objects/update-api-object-kubectl-patch/#use-a-strategic-merge-patch-to-update-a-deployment |  |  |
| `rolloutTemplate` _[RolloutTemplateReference](#rollouttemplatereference)_ | The template reference for this rollout. |  |  |
| `stepBackoffLimit` _integer_ | Specifies the number of retries before declaring a step and this canary<br />rollout as failed. Defaults to 20. | 20 | Minimum: 0 <br /> |
| `suspended` _boolean_ | Suspended disables the canary rollout until the value is cleared. Once<br />resumed, the rollout will continue from the current step. |  |  |




#### CanaryRolloutStep



CanaryRolloutStep defines the actions to be executed for the current step.



_Appears in:_
- [CanaryRolloutTemplateSpec](#canaryrollouttemplatespec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `promoteTo` _[PromoteToRolloutStep](#promotetorolloutstep)_ | Promote the change to group of targets. |  |  |
| `pause` _[PauseRolloutStep](#pauserolloutstep)_ | Pause the rollout. |  |  |
| `analysis` _[CanaryRolloutAnalysis](#canaryrolloutanalysis)_ | Run analysis. |  |  |


#### CanaryRolloutTargetReference



CanaryRolloutPromotedTarget defines a rollout target that has been promoted
to receive the change.



_Appears in:_
- [CanaryRolloutStatus](#canaryrolloutstatus)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiGroup` _string_ | APIGroup is the group for the resource being referenced. |  |  |
| `kind` _string_ | Kind is the type of resource being referenced. |  |  |
| `name` _string_ | Name is the name of resource being referenced |  |  |
| `analysisRun` _[CanaryAnalysisRunInfo](#canaryanalysisruninfo) array_ | Information about performed analysis run against the target. |  |  |


#### CanaryRolloutTemplate



CanaryRolloutTemplate is the Schema for the canaryrollouttemplates API.





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `cp.nuodb.com/v1beta1` | | |
| `kind` _string_ | `CanaryRolloutTemplate` | | |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[CanaryRolloutTemplateSpec](#canaryrollouttemplatespec)_ |  |  |  |


#### CanaryRolloutTemplateSpec



CanaryRolloutTemplateSpec defines the desired state of CanaryRolloutTemplate.



_Appears in:_
- [CanaryRolloutTemplate](#canaryrollouttemplate)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `analysis` _[CanaryRolloutAnalysis](#canaryrolloutanalysis) array_ | Analysis performed after every promotion step. |  |  |
| `skipDisabled` _boolean_ | Skip disabled target resources. By default a change is promoted to all<br />matching resources. |  |  |
| `steps` _[CanaryRolloutStep](#canaryrolloutstep) array_ | Canary rollout steps for this template. |  | MinItems: 1 <br /> |




#### CanaryUpdateStrategy



CanaryUpdateStrategy defines parameters for CanaryRolloutStrategy.



_Appears in:_
- [TierUpdateStrategy](#tierupdatestrategy)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `templateRef` _[LocalObjectReference](#localobjectreference)_ |  |  |  |


#### CasSpec







_Appears in:_
- [IdentityProviderSpec](#identityproviderspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `serverUrl` _string_ | The URL of the CAS server. |  |  |
| `validateEndpoint` _[ValidateEndpoint](#validateendpoint)_ | If specified, the endpoint to use to validate service tickets. If<br />omitted, then the `/serviceValidate` endpoint on the server URL is<br />used to validate service tickets according to the CAS protocol<br />specification. |  |  |


#### ChartSource



ChartSource is the Helm Chart location



_Appears in:_
- [DatabaseSpec](#databasespec)
- [DomainSpec](#domainspec)
- [HelmAppSpec](#helmappspec)
- [ObjectSpecHelm](#objectspechelm)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `repository` _string_ | A https URL to a Helm repo to download the chart from. |  |  |
| `name` _string_ | The Helm chart name available in the remote repository. |  |  |
| `version` _string_ | The version of the chart or semver constraint of the chart to find. |  |  |
| `pinLatestVersion` _boolean_ | Whether to pin the Helm chart version to the latest version currently<br />available in the Helm repository so that future reconciliations doesn't<br />automatically pick up new Helm chart version. This is used only if the<br />Helm chart version is set to empty string ("") which represents the<br />user's intent to use the latest chart version. |  |  |






#### ConfigMapProxyPolicy

_Underlying type:_ _string_

ConfigMapProxyPolicyReconcile controls the lifecycle of the embedded resource.



_Appears in:_
- [ConfigMapProxy](#configmapproxy)

| Field | Description |
| --- | --- |
| `Reconcile` | ConfigMapProxyPolicyReconcile couples the embedded resource lifecycle with<br />the holder ConfigMap lifecycle.<br /> |
| `Create` | ConfigMapProxyPolicyCreate only creates the embedded resource on<br />ConfigMap creation. The embedded resource won't be updated or deleted.<br /> |


#### ConfigurationRestorePolicy

_Underlying type:_ _string_

ConfigurationRestorePolicy defines the way how resources stored in a backup
are restored.

_Validation:_
- Enum: [Merge None]

_Appears in:_
- [DatabaseRestoreSource](#databaserestoresource)

| Field | Description |
| --- | --- |
| `Merge` | MergeRestorePolicy indicates that the operator will try to merge<br />a resource's spec with the one stored in the backup.<br /> |
| `None` | NoneRestorePolicy indicates that the configuration captured by the backup<br />will not be used.<br /> |


#### Database



Database is the Schema for the databases API





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `cp.nuodb.com/v1beta1` | | |
| `kind` _string_ | `Database` | | |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[DatabaseSpec](#databasespec)_ |  |  |  |


#### DatabaseBackup



DatabaseBackup is the Schema for the databasebackups API





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `cp.nuodb.com/v1beta1` | | |
| `kind` _string_ | `DatabaseBackup` | | |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[DatabaseBackupSpec](#databasebackupspec)_ |  |  |  |


#### DatabaseBackupLabelsAssignment



DatabaseBackupLabelsAssignment defines the labels assignment rules for
database backup resource created from database backup policy.



_Appears in:_
- [DatabaseBackupPolicySpec](#databasebackuppolicyspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `fromPolicy` _boolean_ | Assign labels from database backup policy to backups created by this<br />policy. | true |  |
| `fromDatabase` _boolean_ | Assign labels from matching database to backups created by this policy. | true |  |


#### DatabaseBackupPolicy



DatabaseBackupPolicy is the Schema for the databasebackuppolicies API





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `cp.nuodb.com/v1beta1` | | |
| `kind` _string_ | `DatabaseBackupPolicy` | | |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[DatabaseBackupPolicySpec](#databasebackuppolicyspec)_ |  |  |  |


#### DatabaseBackupPolicyMissed







_Appears in:_
- [DatabaseBackupPolicyStatus](#databasebackuppolicystatus)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `missedTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#time-v1-meta)_ | The time that a backup was missed. |  |  |
| `database` _string_ | The database name for which a backup was missed. |  |  |
| `reason` _string_ | A programmatic identifier indicating the reason for missing a backup. |  |  |
| `message` _string_ | A human readable message indicating details about the missed backup. |  |  |


#### DatabaseBackupPolicySpec



DatabaseBackupPolicySpec defines the desired state of DatabaseBackupPolicy.



_Appears in:_
- [DatabaseBackupPolicy](#databasebackuppolicy)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `frequency` _string_ | The backup execution frequency. Allowable values:<br />  - Cron expression, e.g. `0 7 * * *`<br />  - Predefined labels, e.g. `@hourly`, `@daily`, `@weekly`, `@monthly`, `@yearly` |  |  |
| `selector` _[LabelSelector](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#labelselector-v1-meta)_ | A label query over resources for which the backup policy is applied. It<br />must match the resource labels. More info:<br />https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors |  |  |
| `retention` _[BackupRetention](#backupretention)_ | The number of retained artifacts for different frequencies. The number of<br />retained artifacts can only be specified for frequencies of the same or<br />lower granularity than the policy frequency. For example, if the policy<br />frequency is `@daily`, then retention can have values for `daily`,<br />`weekly`, `monthly` and `yearly`, but not for `hourly`. If the policy<br />frequency is `hourly`, then all retention values are allowed. If backup<br />retention is not defined, backups scheduled from this backup policy won't<br />be deleted automatically. |  |  |
| `suspended` _boolean_ | Suspended disables the backup policy temporary so that no backups are<br />scheduled from it. |  |  |
| `pluginName` _string_ | The backup plugin name managing this backup policy. Empty value means<br />that backups from this policy will be executed by the default backup<br />plugin if one is configured. |  |  |
| `startingDeadlineSeconds` _integer_ | Optional deadline in seconds for starting the policy if the scheduled<br />time is missed for any reason. |  |  |
| `backupLabelsAssignment` _[DatabaseBackupLabelsAssignment](#databasebackuplabelsassignment)_ | The backup labels assignment rules. By default backup policy and database<br />labels are assigned to backups scheduled by this policy. |  |  |




#### DatabaseBackupSource



DatabaseBackupSource specifies where a backup will be created from.



_Appears in:_
- [DatabaseBackupSpec](#databasebackupspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `databaseRef` _[LocalObjectReference](#localobjectreference)_ | A reference to the Database object from which a backup should be created.<br />This database is assumed to be in the same namespace as the<br />DatabaseBackup object. This field should be set if the backup does not<br />exists, and needs to be created. This field is immutable after creation. |  |  |
| `backupRef` _[BackupSource](#backupsource)_ | A reference to a pre-existing backup managed by a backup plugin. This<br />field should be set if the backup already exists and only needs a<br />representation in Kubernetes. This field is immutable after creation. |  |  |


#### DatabaseBackupSpec



DatabaseBackupSpec defines the desired state of DatabaseBackup.



_Appears in:_
- [DatabaseBackup](#databasebackup)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `source` _[DatabaseBackupSource](#databasebackupsource)_ | Source holds information about the actual backup. This field is immutable<br />after creation. |  |  |
| `pluginName` _string_ | PluginName is the backup plugin name managing this database backup. Empty<br />value means that this backup will be executed by the default backup<br />plugin if one is configured. |  |  |




#### DatabaseComponentsStatus



DatabaseComponentsStatus defines the observed state of Database components



_Appears in:_
- [DatabaseStatus](#databasestatus)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `transactionEngines` _[WorkloadStatus](#workloadstatus) array_ | Transaction Engine component status information. |  |  |
| `storageManagers` _[WorkloadStatus](#workloadstatus) array_ | Storage Manager component status information. |  |  |
| `lastUpdateTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#time-v1-meta)_ | Last update timestamp for this status. |  |  |


#### DatabaseQuota



DatabaseQuota is the Schema for the databasequota API





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `cp.nuodb.com/v1beta1` | | |
| `kind` _string_ | `DatabaseQuota` | | |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[DatabaseQuotaSpec](#databasequotaspec)_ |  |  |  |


#### DatabaseQuotaSpec



DatabaseQuotaSpec defines the desired state of DatabaseQuota



_Appears in:_
- [DatabaseQuota](#databasequota)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `scope` _[QuotaScope](#quotascope)_ | The scope to which the quota resource limits are applied. This<br />enables defining out of band quota configuration on database<br />resources filtered and grouped by the supplied criteria. |  |  |




#### DatabaseRestoreSource



DatabaseRestoreSource specifies where to restore the database from.



_Appears in:_
- [DatabaseSpec](#databasespec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `backupRef` _[LocalObjectReference](#localobjectreference)_ | A reference to the DatabaseBackup resource from which to populate the<br />database state. |  |  |
| `databaseRestorePolicy` _[ConfigurationRestorePolicy](#configurationrestorepolicy)_ | The Database resource restore policy. By default, the database<br />spec will be merged with the one stored in the backup if possible. | Merge | Enum: [Merge None] <br /> |
| `maxRetries` _integer_ | Maximum number of retries that should be attempted on failure before<br />giving up. Set to zero or negative number to disable<br />retries. | 20 |  |
| `backOffSec` _integer_ | The backoff duration in seconds after failed restore operation. The total<br />backoff interval will be multiplied by the number of failures. | 30 |  |


#### DatabaseSpec



DatabaseSpec defines the desired state of Database



_Appears in:_
- [Database](#database)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `chart` _[ChartSource](#chartsource)_ | The Helm Chart source |  |  |
| `template` _[ReleaseTemplate](#releasetemplate)_ | Additional configuration for the Helm release |  |  |
| `type` _[ServiceType](#servicetype)_ | Database instance service type |  |  |
| `version` _string_ | NuoDB image version used for the database |  |  |
| `dbName` _string_ | The name use for this database |  |  |
| `domainRef` _[LocalObjectReference](#localobjectreference)_ | Reference pointing to the name of the NuoDB domain associated with this<br />database instance |  |  |
| `passwordRef` _[ValueReference](#valuereference)_ | Reference pointing to the name of the Secret holding the DBA password |  |  |
| `hostname` _string_ | FQDN for the database endpoint |  |  |
| `archiveVolume` _[PersistentStorage](#persistentstorage)_ | ArchiveVolume configures the database archive volume. |  |  |
| `journalVolume` _[PersistentStorage](#persistentstorage)_ | JournalVolume configures the database external journal volume. If<br />defined, a separate volume for the database journal will be provisioned. |  |  |
| `maintenance` _[MaintenanceConfig](#maintenanceconfig)_ | The maintenance configuration for the database. |  |  |
| `restoreFrom` _[DatabaseRestoreSource](#databaserestoresource)_ | RestoreFrom indicates that the database should be restored from a<br />backup rather than having an empty state. |  |  |




#### Domain



Domain is the Schema for the domains API





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `cp.nuodb.com/v1beta1` | | |
| `kind` _string_ | `Domain` | | |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[DomainSpec](#domainspec)_ |  |  |  |


#### DomainComponentsStatus



DomainComponentsStatus defines the observed state of Domain components



_Appears in:_
- [DomainStatus](#domainstatus)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `admins` _[WorkloadStatus](#workloadstatus) array_ | NuoDB Admin component status information. |  |  |
| `lastUpdateTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#time-v1-meta)_ | Last update timestamp for this status. |  |  |


#### DomainSpec



DomainSpec defines the desired state of Domain



_Appears in:_
- [Domain](#domain)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `chart` _[ChartSource](#chartsource)_ | The Helm Chart source |  |  |
| `template` _[ReleaseTemplate](#releasetemplate)_ | Additional configuration for the Helm release |  |  |
| `type` _[ServiceType](#servicetype)_ | Domain instance service type |  |  |
| `version` _string_ | NuoDB image version used for the domain |  |  |
| `sqlHostname` _string_ | FQDN for the endpoint used by the external SQL clients |  |  |
| `tls` _[TLSConfig](#tlsconfig)_ | The Transport Layer Security (TLS) configuration for the domain and all<br />databases that are part of it. |  |  |
| `maintenance` _[MaintenanceConfig](#maintenanceconfig)_ | The maintenance configuration for the domain. |  |  |




#### HelmApp



HelmApp is the Schema for the helmapps API





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `cp.nuodb.com/v1beta1` | | |
| `kind` _string_ | `HelmApp` | | |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[HelmAppSpec](#helmappspec)_ |  |  |  |


#### HelmAppComponentsStatus



HelmAppComponentsStatus defines the observed state of HelmApp components.



_Appears in:_
- [HelmAppStatus](#helmappstatus)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `workloads` _[WorkloadStatus](#workloadstatus) array_ | Workloads define the observed status for all statefulsets and deployments<br />installed by this HelmApp. |  |  |
| `lastUpdateTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#time-v1-meta)_ | Last update timestamp for this status. |  |  |


#### HelmAppSpec



HelmAppSpec defines the desired state of HelmApp



_Appears in:_
- [HelmApp](#helmapp)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `source` _[ChartSource](#chartsource)_ | Source defines the Helm chart location. |  |  |
| `template` _[ReleaseTemplate](#releasetemplate)_ | Template provides additional configuration for the Helm release. |  |  |
| `valuesRefs` _[ValueReference](#valuereference) array_ | ValuesRefs are references to ConfigMap or Secret resources in the local<br />namespace to check for user-supplied Helm values. |  |  |




#### HelmFeature



HelmFeature is the Schema for the helmfeatures API





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `cp.nuodb.com/v1beta1` | | |
| `kind` _string_ | `HelmFeature` | | |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[HelmFeatureSpec](#helmfeaturespec)_ |  |  |  |


#### HelmFeatureParamDef



HelmFeatureParamDef defines the schema for Helm feature parameter.



_Appears in:_
- [HelmFeatureSpec](#helmfeaturespec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `default` _string_ | The parameter default value. Defaults to empty string if not<br />defined. |  |  |
| `jsonSchema` _string_ | A JSONSchema used to validate the parameter's value. |  |  |
| `description` _string_ | The parameter's description. |  |  |


#### HelmFeatureReference



A Helm feature referenced by a service tier.



_Appears in:_
- [ServiceTierReference](#servicetierreference)
- [ServiceTierSpec](#servicetierspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `name` _string_ | The name of the resource. |  |  |
| `namespace` _string_ | The namespace of the resource. When not specified, the current<br />namespace is assumed. |  |  |
| `revision` _string_ | Revision of the Helm feature used by this revision of the service tier. |  | MinLength: 1 <br /> |


#### HelmFeatureSpec



HelmFeatureSpec defines the desired state of HelmFeature



_Appears in:_
- [HelmFeature](#helmfeature)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `chartCompatibility` _string_ | The Helm chart version compatibility constraint for the Helm feature. |  |  |
| `productCompatibility` _string_ | The NuoDB product version compatibility constraint for the<br />Helm feature. |  |  |
| `optional` _boolean_ | Whether the Helm feature is optional and does not emit an error<br />if the Helm chart or product version is incompatible. |  |  |
| `parameters` _object (keys:string, values:[HelmFeatureParamDef](#helmfeatureparamdef))_ | The parameter definitions referenced in values. For example, parameter<br />named `foo` is referenced using `<< .meta.params.foo >>` template. |  |  |
| `values` _[JSON](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#json-v1-apiextensions-k8s-io)_ | The Helm values that enable the feature. |  |  |




#### HttpHeader



HTTP header configuration.



_Appears in:_
- [PrometheusMetricProvider](#prometheusmetricprovider)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `key` _string_ | The HTTP header key. |  |  |
| `value` _string_ | The HTTP header value. |  |  |


#### IdentityProvider



IdentityProvider is the Schema for the identityproviders API.





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `cp.nuodb.com/v1beta1` | | |
| `kind` _string_ | `IdentityProvider` | | |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[IdentityProviderSpec](#identityproviderspec)_ |  |  |  |


#### IdentityProviderSpec



IdentityProviderSpec defines the desired state of IdentityProvider.



_Appears in:_
- [IdentityProvider](#identityprovider)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `oidc` _[OidcSpec](#oidcspec)_ | Specification for the OpenID Connect (OIDC) provider. |  |  |
| `cas` _[CasSpec](#casspec)_ | Specification for the Central Authentication Service (CAS) provider. |  |  |
| `provisionUser` _[ProvisionUser](#provisionuser)_ | Rules for resolving the user to provision in the NuoDB Control Plane<br />bound to the user authenticated by the external provider. If the user<br />with the resolved organization and name does not exist, then one will<br />be created with the resolved roles and access rule the first time it<br />is authenticated by the REST server. |  |  |




#### KeyPairType

_Underlying type:_ _string_

KeyPairType defines the asymmetric encryption algorithm for key-pair.

_Validation:_
- Enum: [RSA ECDSA]

_Appears in:_
- [NuoDBTlsProviderConfig](#nuodbtlsproviderconfig)

| Field | Description |
| --- | --- |
| `RSA` |  |
| `ECDSA` |  |


#### KeyStrength

_Underlying type:_ _string_

KeyStrength defines the strength of the key, which corresponds to a
particular size in bits for each algorithm.

_Validation:_
- Enum: [WEAK MEDIUM STRONG VERY_STRONG]

_Appears in:_
- [NuoDBTlsProviderConfig](#nuodbtlsproviderconfig)

| Field | Description |
| --- | --- |
| `WEAK` | KeyStrengthWeak corresponds to key size - RSA 1024, EC 256<br /> |
| `MEDIUM` | KeyStrengthMedium corresponds to key size - RSA 2048, EC 256<br /> |
| `STRONG` | KeyStrengthStrong corresponds to key size - RSA 2048, EC 384<br /> |
| `VERY_STRONG` | KeyStrengthVeryStrong corresponds to key size - RSA 3072, EC 521<br /> |


#### LocalObjectReference



LocalObjectReference locates the referenced object inside the same namespace



_Appears in:_
- [BasicAuthenticationConfig](#basicauthenticationconfig)
- [CanaryUpdateStrategy](#canaryupdatestrategy)
- [DatabaseBackupSource](#databasebackupsource)
- [DatabaseRestoreSource](#databaserestoresource)
- [DatabaseSpec](#databasespec)
- [RolloutTemplateReference](#rollouttemplatereference)
- [TLSConfig](#tlsconfig)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `name` _string_ | Name of the referent |  |  |


#### MaintenanceConfig



MaintenanceConfig defines whether domain or database is disabled or should be
disabled at some time in the future.



_Appears in:_
- [DatabaseSpec](#databasespec)
- [DomainSpec](#domainspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `expiresAtTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#time-v1-meta)_ | The time at which to mark the domain or database as being disabled. |  |  |
| `expiresIn` _[Duration](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#duration-v1-meta)_ | The time delta until the domain or database is marked as being<br />disabled. This value is used to calculate the ExpiresAtTime value<br />that is injected by the controller on creation or update. |  | Pattern: `^([0-9]+(\.[0-9]+)?(ns\|us\|µs\|ms\|s\|m\|h))+$` <br />Type: string <br /> |
| `isDisabled` _boolean_ | Whether to disable the domain or database by scaling down all<br />associated workloads to replicas=0. | false |  |
| `shouldShutdownGracefully` _boolean_ | Whether to gracefully shutdown domain or database workloads. This<br />causes all database workloads to be shutdown before domain workload,<br />with TEs being shutdown before SMs. This has no effect if the domain<br />or database is not disabled. | true |  |


#### Metric



Metric is the Schema for the metrics API.





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `cp.nuodb.com/v1beta1` | | |
| `kind` _string_ | `Metric` | | |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[MetricSpec](#metricspec)_ |  |  |  |


#### MetricDescriptor



MetricDescriptor defines a metric type and its schema.



_Appears in:_
- [MetricSpec](#metricspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `name` _string_ | The name of the metric. |  |  |
| `unit` _string_ | The units in which the metric value is reported. |  |  |
| `description` _string_ | A detailed description of the metric. |  |  |
| `internalOnly` _boolean_ | Whether the metric is internal only or exposed to DBaaS users. |  |  |
| `productCompatibility` _string_ | The NuoDB product version compatibility constraint for the metric. |  |  |
| `dimensions` _[MetricDimension](#metricdimension) array_ | A set of custom dimensions for classifying metric's data. |  |  |
| `prometheus` _[PrometheusMetric](#prometheusmetric)_ | Prometheus specific metric configuration. |  |  |


#### MetricDimension



MetricDimension defines metric dimension configuration.



_Appears in:_
- [MetricDescriptor](#metricdescriptor)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `name` _string_ | The metric dimension's name. |  |  |
| `description` _string_ | A detailed description of the metric dimension. |  |  |
| `jsonSchema` _string_ | A JSONSchema used to validate the dimension's value. |  |  |


#### MetricSource



MetricSource is the Schema for the metricsources API.





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `cp.nuodb.com/v1beta1` | | |
| `kind` _string_ | `MetricSource` | | |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[MetricSourceSpec](#metricsourcespec)_ |  |  |  |


#### MetricSourceProvider



MetricSourceProvider defines connection infromation for the metric source
provider.



_Appears in:_
- [MetricSourceSpec](#metricsourcespec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `prometheus` _[PrometheusMetricProvider](#prometheusmetricprovider)_ | Configuration for Prometheus server metrics provider. |  |  |


#### MetricSourceSpec



MetricSourceSpec defines the desired state of MetricSource.



_Appears in:_
- [MetricSource](#metricsource)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `targetsSelector` _[LabelSelector](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#labelselector-v1-meta)_ | A label query over target resources for which the metric source applies.<br />It must match the resource labels. If not specified, matches all targets<br />in the same namespace. More info:<br />https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors |  |  |
| `metricSelector` _[LabelSelector](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#labelselector-v1-meta)_ | A label query over metric resources for which the metric source applies.<br />It must match the resource labels. If not specified, matches all metric<br />resources in the same namespace. More info:<br />https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors |  |  |
| `provider` _[MetricSourceProvider](#metricsourceprovider)_ | Metric source provider configuration. |  |  |




#### MetricSpec



MetricSpec defines the desired state of Metric.



_Appears in:_
- [Metric](#metric)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `metrics` _[MetricDescriptor](#metricdescriptor) array_ | A list of metric descriptors. |  | MinItems: 1 <br /> |




#### NamespacedObjectReference



NamespacedObjectReference contains enough information to let you locate
the referenced object in any namespace



_Appears in:_
- [HelmFeatureReference](#helmfeaturereference)
- [ServiceTierReference](#servicetierreference)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `name` _string_ | The name of the resource. |  |  |
| `namespace` _string_ | The namespace of the resource. When not specified, the current<br />namespace is assumed. |  |  |


#### NuoDBTlsProviderConfig



NuoDBTlsProviderConfig is the configuration for the NuoDBControlPlane
provider.



_Appears in:_
- [TlsGenerateConfig](#tlsgenerateconfig)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `keyType` _[KeyPairType](#keypairtype)_ | KeyType is the asymmetric encryption algorithm for the generated<br />key-pair. | RSA | Enum: [RSA ECDSA] <br /> |
| `keyStrength` _[KeyStrength](#keystrength)_ | KeyStrength is the strength of the generated key. | MEDIUM | Enum: [WEAK MEDIUM STRONG VERY_STRONG] <br /> |
| `validity` _[Duration](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#duration-v1-meta)_ | Validity is the lifetime of the server certificate. Defaults to 1 year.<br />The parsed duration is rounded up to number of days. Minimum accepted<br />duration is 1 day. |  | Pattern: `^([0-9]+(\.[0-9]+)?(ns\|us\|µs\|ms\|s\|m\|h))+$` <br />Type: string <br /> |
| `renewBeforeExpiration` _[Duration](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#duration-v1-meta)_ | RenewBeforeExpiration defines how long before the currently issued TLS<br />keys's expiry, they need to be renewed. Defaults to 1/3 of the<br />certificates validity or max 7 days before expiration. |  | Pattern: `^([0-9]+(\.[0-9]+)?(ns\|us\|µs\|ms\|s\|m\|h))+$` <br />Type: string <br /> |
| `renewPasswords` _boolean_ | RenewPasswords indicates whether the Java keystore passwords must be<br />changed along with the certificates. Changing the passwords requires<br />NuoAdmin restart when TLS certificates are rotated. |  |  |






#### ObjectSpecHelm



ObjectSpecHelm is a Helm specific configuration that every ObjectWithRelease
object must have



_Appears in:_
- [DatabaseSpec](#databasespec)
- [DomainSpec](#domainspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `chart` _[ChartSource](#chartsource)_ | The Helm Chart source |  |  |
| `template` _[ReleaseTemplate](#releasetemplate)_ | Additional configuration for the Helm release |  |  |


#### ObjectStatusHelm



ObjectStatusHelm is a Helm specific status that every ObjectWithRelease
object must have



_Appears in:_
- [HelmAppStatus](#helmappstatus)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `release` _[ReleaseInfo](#releaseinfo)_ | Release holds status information about the Helm release associated with<br />the resource. |  |  |


#### ObjectStatusReleaseOwner



ObjectStatusReleaseOwner should be embedded in objects that have dependant
HelmApp resources.



_Appears in:_
- [DatabaseStatus](#databasestatus)
- [DomainStatus](#domainstatus)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `releaseRefs` _[ReleaseReference](#releasereference) array_ | ReleaseRefs contain references to the dependant HelmApp resources that<br />have this object as an owner. Expected to be non-empty once the<br />corresponding applications are installed. |  |  |










#### OidcSpec







_Appears in:_
- [IdentityProviderSpec](#identityproviderspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `issuerUrl` _string_ | The URL of the OIDC provider. |  |  |
| `clientId` _[ValueOrSecretReference](#valueorsecretreference)_ | The client ID to use for the OIDC provider. |  |  |
| `clientSecret` _[SecretReference](#secretreference)_ | The Secret resource reference to the client secret to use for the<br />OIDC provider. |  |  |
| `updateInterval` _[Duration](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#duration-v1-meta)_ | The interval at which the OIDC provider configuration is updated via<br />OpenID Connect discovery. |  |  |
| `tlsSkipVerify` _boolean_ | Whether to disable TLS verification of the server certificate. |  |  |


#### OidcStatus







_Appears in:_
- [IdentityProviderStatus](#identityproviderstatus)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `issuerUrl` _string_ | The URL of the OIDC provider. |  |  |
| `configuration` _string_ | The content returned by the OpenID Connect discovery endpoint, which<br />is `<issuerUrl>/.well-known/openid-configuration`. |  |  |
| `jwks` _string_ | The content returned by the JSON Web Key Set (JWKS) endpoint<br />appearing in the `jwks_uri` property of OIDC configuration. |  |  |
| `authorizationEndpoint` _string_ | The `authorization_endpoint` property of OIDC configuration. |  |  |
| `tokenEndpoint` _string_ | The `token_endpoint` property of OIDC configuration. |  |  |
| `lastUpdateTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#time-v1-meta)_ | The last update time for the OIDC configuration. |  |  |
| `nextUpdateTime` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#time-v1-meta)_ | The time that the next update will be scheduled for the OIDC<br />configuration. |  |  |
| `error` _string_ | The error that occurred while obtaining OIDC configuration. |  |  |
| `errorCount` _integer_ | The number of consecutive attempts to obtain OIDC configuration that<br />have failed. |  |  |


#### PauseRolloutStep



PauseRolloutStep pauses the rollout.



_Appears in:_
- [CanaryRolloutStep](#canaryrolloutstep)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `duration` _[Duration](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#duration-v1-meta)_ | The duration for which the rollout is paused. Zero duration means wait<br />until manually approved. |  | Pattern: `^([0-9]+(\.[0-9]+)?(ns\|us\|µs\|ms\|s\|m\|h))+$` <br />Type: string <br /> |


#### PersistentStorage



PersistentStorage defines the storage configuration for a persistent volume.



_Appears in:_
- [DatabaseSpec](#databasespec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `volumeSize` _[Quantity](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#quantity-resource-api)_ | VolumeSize is the storage resource request, in bytes (e,g. 5Gi = 5GiB = 5<br />* 1024 * 1024 * 1024) |  |  |
| `storageClassName` _string_ | StorageClassName is the name of the StorageClass required for this<br />volume. |  |  |
| `dataSourceRef` _[TypedObjectReference](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#typedobjectreference-v1-core)_ | DataSourceRef specifies the object from which to populate the volume with<br />data, if a non-empty volume is desired. An existing VolumeSnapshot object<br />(snapshot.storage.k8s.io/VolumeSnapshot) or an existing PVC<br />(PersistentVolumeClaim) are supported. |  |  |


#### PersistentVolumeClaimRetentionPolicy

_Underlying type:_ _string_





_Appears in:_
- [ReleaseTemplate](#releasetemplate)

| Field | Description |
| --- | --- |
| `Delete` | PersistentVolumeClaimRetentionDelete means the persistent volume claims<br />will be deleted after the release is uninstalled. The associated<br />persistent volume retention is controlled separately.<br /> |
| `Retain` | PersistentVolumeClaimRetentionRetain means the persistent volume claims<br />will be left in their current state for manual removal by the<br />administrator. The associated persistent volume retention is controlled<br />separately.<br /> |


#### PrometheusMetric



PrometheusMetric defines a Prometheus metric query parameters.



_Appears in:_
- [MetricDescriptor](#metricdescriptor)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `query` _string_ | The Prometheus query string using Prometheus Query Language (PromQL).<br />More info: https://prometheus.io/docs/prometheus/latest/querying/basics/ |  |  |


#### PrometheusMetricProvider



Defines connection information for a Prometheus server.



_Appears in:_
- [MetricSourceProvider](#metricsourceprovider)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `address` _string_ | The HTTP URL of the Prometheus server. |  |  |
| `authentication` _[AuthenticationMethod](#authenticationmethod)_ | The authentication method used when communicating with Prometheus<br />server's query APIs. |  |  |
| `timeoutSec` _integer_ | The duration in seconds within which a prometheus query should complete. |  | Minimum: 0 <br /> |
| `insecureSkipVerify` _boolean_ | Skip TLS hostname verification. |  |  |
| `headers` _[HttpHeader](#httpheader) array_ | Optional HTTP headers to use in the request. |  |  |


#### PromoteToRolloutStep



PromoteToStep defines the target resources to which a change is promoted in
parallel and rollback behaviour in case of failed analysis.



_Appears in:_
- [CanaryRolloutStep](#canaryrolloutstep)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `labelSelector` _[LabelSelector](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#labelselector-v1-meta)_ | A label query over resources to which promotion is performed. It must<br />match the resource labels. The label selector requirements are ANDed with<br />those defined in the canary rollout selector. |  |  |
| `limitCount` _integer_ | Limit the promotion to certain number of the matching resources. The<br />supplied limit is cumulative across promote steps (i.e. total number of<br />targets to be promoted). |  | Minimum: 1 <br /> |
| `limitPercentage` _integer_ | Limit the promotion to certain percentage of the matching resources. The<br />supplied limit is cumulative across promote steps (i.e. total percentage<br />of targets to be promoted). |  | Maximum: 100 <br />Minimum: 1 <br /> |
| `rollback` _[RollbackOptions](#rollbackoptions)_ | Actions performed on failed analysis. No automatic rollback is performed<br />by default. |  |  |


#### ProvisionUser







_Appears in:_
- [IdentityProviderSpec](#identityproviderspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `organization` _[ValueOrResolvedValue](#valueorresolvedvalue)_ | Resolver for the organization the user belongs to. |  |  |
| `name` _[ValueOrResolvedValue](#valueorresolvedvalue)_ | Resolver for the user name. |  |  |
| `roles` _[ValueOrResolvedValue](#valueorresolvedvalue) array_ | Resolvers for roles assigned to the user, which are aggregated to<br />obtain the full list of roles assigned to the user. |  |  |
| `accessRule` _[ValueOrPath](#valueorpath)_ | Resolver for the access rule of the user. |  |  |
| `validate` _[Validate](#validate) array_ | Validations to apply to the user attributes from the external provider. |  |  |




#### QuotaEnforcementRecord







_Appears in:_
- [DatabaseQuotaStatus](#databasequotastatus)
- [QuotaStatus](#quotastatus)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `enforceTimestamp` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#time-v1-meta)_ | Timestamp is a timestamp representing the server time when this quota was<br />enforced on a selected object. |  |  |
| `objectRef` _[TypedLocalObjectReference](#typedlocalobjectreference)_ | ObjectRef is a reference to the object on which this quota was enforced. |  |  |
| `objectGeneration` _integer_ | The generation that the object had at the time of quota enforcement. |  |  |


#### QuotaScope



QuotaScope defines the criteria for selecting resources and dividing them
into groups. The quota resource limits are applied to each individual group.
The supplied filtering criteria are ANDed. If none of labelSelector or
fieldSelector is specified all databases in the namespace will be selected.



_Appears in:_
- [DatabaseQuotaSpec](#databasequotaspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `labelSelector` _[LabelSelector](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#labelselector-v1-meta)_ | A label query over resources for which the quota is applied. It must<br />match the resource labels. More info:<br />https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors |  |  |
| `fieldSelector` _[FieldsSelector](#fieldsselector)_ | A field query over resources for which the quota is applied. It must<br />match the resource fields. Supported fields are "spec.type.sla" and<br />"spec.type.tierRef.name". More info:<br />https://kubernetes.io/docs/concepts/overview/working-with-objects/field-selectors/ |  |  |
| `groupByLabels` _string array_ | The label keys on which the selected databases are divided into<br />groups. |  |  |


#### QuotaStatus



QuotaStatus defines the Quota observed state.



_Appears in:_
- [DatabaseQuotaStatus](#databasequotastatus)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `lastEnforced` _[QuotaEnforcementRecord](#quotaenforcementrecord) array_ | The information about objects on which this quota has been enforced.<br />It is cleared by the quota controller after a successful<br />reconciliation. |  |  |
| `observedGeneration` _integer_ | The last observed generation. |  |  |


#### ReleaseInfo



ReleaseInfo defines the observed state of the Helm release associated with an
object



_Appears in:_
- [HelmAppStatus](#helmappstatus)
- [ObjectStatusHelm](#objectstatushelm)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `observedGeneration` _integer_ | The last observed generation. |  |  |
| `failures` _integer_ | Failures is the reconciliation failure count against the latest desired<br />state. It is reset after a successful reconciliation |  |  |
| `lastReleaseRevision` _integer_ | The revision of the last successful Helm release |  |  |
| `lastAttemptedChartVersion` _string_ | The chart version used in the last reconciliation attempt |  |  |
| `lastAttemptedValuesChecksum` _string_ | The SHA1 checksum of the values used in the last reconciliation attempt |  |  |


#### ReleaseReference



ReleaseReference locates the referenced Helm release object in the same namespace.



_Appears in:_
- [DatabaseStatus](#databasestatus)
- [DomainStatus](#domainstatus)
- [ObjectStatusReleaseOwner](#objectstatusreleaseowner)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiGroup` _string_ | APIGroup is the group for the resource being referenced. |  |  |
| `kind` _string_ | Kind is the type of resource being referenced. |  |  |
| `name` _string_ | Name is the name of resource being referenced |  |  |
| `releaseName` _string_ | The name of the Helm release. |  |  |
| `releaseNamespace` _string_ | The target namespace of the Helm release. |  |  |
| `synced` _boolean_ | Whether the Helm release has been synchronized. |  |  |
| `lastReleaseRevision` _integer_ | The revision of the last successful Helm release. |  |  |


#### ReleaseTemplate



ReleaseTemplate holds the configuration for the Helm release



_Appears in:_
- [DatabaseSpec](#databasespec)
- [DomainSpec](#domainspec)
- [HelmAppSpec](#helmappspec)
- [ObjectSpecHelm](#objectspechelm)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `releaseName` _string_ | The name of the Helm release |  |  |
| `namespace` _string_ | The target namespace to install the Helm release in |  |  |
| `maxRetries` _integer_ | Maximum number of retries that should be attempted on failures before<br />giving up. Defaults to 20. Set to negative number to disable retries. | 20 |  |
| `backOffSec` _integer_ | The backoff duration in seconds after failed helm install/upgrade. The<br />total backoff interval will be multiplied by the number of failures. | 60 |  |
| `dataRetentionPolicy` _[PersistentVolumeClaimRetentionPolicy](#persistentvolumeclaimretentionpolicy)_ | Defines what happens with the persistent volume claims after the Helm<br />release is uninstalled. Defaults to 'Delete' which means that all<br />associated PVCs are removed. | Delete | Enum: [Delete Retain] <br /> |






#### RevisionHistory



Revision history maintained for the resource.



_Appears in:_
- [HelmFeatureStatus](#helmfeaturestatus)
- [ServiceTierStatus](#servicetierstatus)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `revisions` _[SpecRevision](#specrevision) array_ | Resource revisions. |  |  |


#### RoleTemplate



RoleTemplate is the Schema for the roletemplates API.





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `cp.nuodb.com/v1beta1` | | |
| `kind` _string_ | `RoleTemplate` | | |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[RoleTemplateSpec](#roletemplatespec)_ |  |  |  |


#### RoleTemplateSpec



RoleTemplateSpec defines the desired state of RoleTemplate.



_Appears in:_
- [RoleTemplate](#roletemplate)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `allow` _[AccessRuleEntry](#accessruleentry) array_ | List of access rule entries to allow. |  | MinItems: 1 <br /> |




#### RollbackOptions



RollbackOptions defines the rollback parameters.



_Appears in:_
- [PromoteToRolloutStep](#promotetorolloutstep)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `strategy` _[RollbackStrategy](#rollbackstrategy)_ | The rollback strategy. | Failed | Enum: [None Failed Step] <br /> |
| `backoffLimit` _integer_ | Specifies the number of retries before giving up on rollback. Defaults to 20. | 20 | Minimum: 0 <br /> |


#### RollbackStrategy

_Underlying type:_ _string_

RollbackStrategy defines the actions to be performed on failed analysis.

_Validation:_
- Enum: [None Failed Step]

_Appears in:_
- [RollbackOptions](#rollbackoptions)



#### RolloutTemplateReference



A rollout template referenced by canary rollout.



_Appears in:_
- [CanaryRolloutSpec](#canaryrolloutspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `name` _string_ | Name of the referent |  |  |


#### SecretReference







_Appears in:_
- [OidcSpec](#oidcspec)
- [ValueOrSecretReference](#valueorsecretreference)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `name` _string_ | The name of the Secret resource to obtain the value from. |  | MinLength: 1 <br /> |
| `key` _string_ | The key of the value within the Secret resource. |  | MinLength: 1 <br /> |


#### ServiceTier



ServiceTier is the Schema for the servicetiers API





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `cp.nuodb.com/v1beta1` | | |
| `kind` _string_ | `ServiceTier` | | |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[ServiceTierSpec](#servicetierspec)_ |  |  |  |


#### ServiceTierReference



ServiceTierReference contains a reference to a ServiceTier resource in the
same or a different namespace.



_Appears in:_
- [ServiceType](#servicetype)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `name` _string_ | The name of the resource. |  |  |
| `namespace` _string_ | The namespace of the resource. When not specified, the current<br />namespace is assumed. |  |  |
| `parameters` _object (keys:string, values:string)_ | Opaque parameters passed to the Helm features of the referenced service<br />tier. |  |  |
| `revision` _string_ | Revision of the service tier. |  | MinLength: 1 <br /> |
| `featureOverrides` _[HelmFeatureReference](#helmfeaturereference) array_ | Features that override the service tier Helm values for this resource. |  |  |


#### ServiceTierSpec



ServiceTierSpec defines the desired state of ServiceTier



_Appears in:_
- [ServiceTier](#servicetier)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `features` _[HelmFeatureReference](#helmfeaturereference) array_ | The list of Helm features enabled for this service tier. |  |  |
| `updateStrategy` _[TierUpdateStrategy](#tierupdatestrategy)_ | The service tier update strategy used by the controller to deliver<br />changes in the service tier or referenced features to domain and<br />databases. |  |  |




#### ServiceType



ServiceType provides the service instance configuration information



_Appears in:_
- [DatabaseSpec](#databasespec)
- [DomainSpec](#domainspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `tierRef` _[ServiceTierReference](#servicetierreference)_ | The service instance tier type |  |  |
| `sla` _[SlaType](#slatype)_ | The service instance SLA type |  |  |


#### SlaType

_Underlying type:_ _string_

ServiceTierType is the type of the NuoDB instance service level agreements
(SLA) associated with the service



_Appears in:_
- [ServiceType](#servicetype)

| Field | Description |
| --- | --- |
| `prod` | SLA used for production service instances which requires no downtime, RPO<br />of 15 min and RTO of 2 hrs (depends on the instance size).<br /> |
| `qa` | SLA used for test/qa/staging service instances which requires scheduled<br />downtime only, RPO of 4 hrs and RTO of 4 hrs (depends on the instance size).<br /> |
| `dev` | SLA used for development service instances which tolerate unscheduled<br />downtime, RPO of 12 hrs and RTO of 6 hrs (depends on the instance size).<br /> |


#### SpecRevision



Desired state revision of a resource.



_Appears in:_
- [RevisionHistory](#revisionhistory)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `spec` _integer array_ | The encoded versioned resource desired state. |  |  |
| `generation` _integer_ | A sequence number representing a specific generation of the desired<br />state stored in the revision. |  |  |
| `creationTimestamp` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#time-v1-meta)_ | A timestamp representing the server time when this version was created. |  |  |


#### StatusConditionAnalysis



StatusConditionAnalysis requires a certain status condition on the target
resource.



_Appears in:_
- [CanaryRolloutAnalysis](#canaryrolloutanalysis)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `type` _string_ | The condition type to perform analysis on. |  |  |
| `timeout` _[Duration](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/#duration-v1-meta)_ | A timeout after which an analysis is declared as failed. |  | Pattern: `^([0-9]+(\.[0-9]+)?(ns\|us\|µs\|ms\|s\|m\|h))+$` <br />Type: string <br /> |


#### TLSConfig



TLSConfig defines the Transport Layer Security (TLS) configuration for the
Domain



_Appears in:_
- [DomainSpec](#domainspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `secretRef` _[LocalObjectReference](#localobjectreference)_ | SecretRef is a reference to the location of the Secret providing the<br />domain TLS configuration. |  |  |
| `keystoreKey` _string_ | The key in the Secret that provides the contents of the Java keystore<br />file. | nuoadmin.p12 |  |
| `truststoreKey` _string_ | The key in the Secret that provides the contents of the Java truststore<br />file. | nuoadmin-truststore.p12 |  |
| `keystorePasswordKey` _string_ | The key in the Secret that provides the password for the Java keystore. | keystorePassword |  |
| `truststorePasswordKey` _string_ | The key in the Secret that provides the password for the Java truststore. | truststorePassword |  |
| `clientCertKey` _string_ | The key in the Secret that provides the certificate and private key in<br />PEM format used by the NuoDB Admin REST clients. | nuocmd.pem |  |
| `caCertKey` _string_ | The key in the Secret that provides the Certificate Authority (CA) X509<br />certificate bundle that has signed the NuoDB Admin server key and used by<br />the NuoDB Admin REST clients. Leave it empty if a public CA has been<br />used. | ca.cert |  |
| `generate` _[TlsGenerateConfig](#tlsgenerateconfig)_ | Automatically generate and provision the TLS keys in the configured<br />Secret reference. |  |  |


#### TierUpdateStrategy



TierUpdateStrategy defines the strategy that the ServiceTier controller will
use to deliver updates of the referenced Helm features to Domain and Databae
resources.



_Appears in:_
- [ServiceTierSpec](#servicetierspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `type` _[TierUpdateStrategyType](#tierupdatestrategytype)_ | The service tier update strategy type. Defaults to Immediate. |  | Enum: [CanaryRollout Immediate] <br /> |
| `canary` _[CanaryUpdateStrategy](#canaryupdatestrategy)_ | Parameters for CanaryRollout update strategy. |  |  |


#### TierUpdateStrategyType

_Underlying type:_ _string_

TierUpdateStrategyType is a string type that enumerates all possible update
strategies for the ServiceTier controller.

_Validation:_
- Enum: [CanaryRollout Immediate]

_Appears in:_
- [TierUpdateStrategy](#tierupdatestrategy)

| Field | Description |
| --- | --- |
| `CanaryRollout` | CanaryRolloutStrategy indicates that changes to service tier or<br />referenced features will be delivered to domains and databases<br />progressively by creating CanaryRollout resource.<br /> |
| `Immediate` | ImmediateStrategy indicates that changes to service tier or referenced<br />features will be effective to domains and databases immediately.<br /> |


#### TlsGenerateConfig



TlsGenerateConfig defines the TLS auto generation configuration.



_Appears in:_
- [TLSConfig](#tlsconfig)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `provider` _[TlsProvider](#tlsprovider)_ | The TLS configuration provider. |  | Enum: [NUODB_CP] <br /> |
| `nuodbConfig` _[NuoDBTlsProviderConfig](#nuodbtlsproviderconfig)_ | The configuration for the NuoDBControlPlane provider |  |  |




#### TlsProvider

_Underlying type:_ _string_

TlsProvider defines the strategy that will be used to generate the TLS
configuration.

_Validation:_
- Enum: [NUODB_CP]

_Appears in:_
- [TlsGenerateConfig](#tlsgenerateconfig)

| Field | Description |
| --- | --- |
| `NUODB_CP` | NuoDB Control Plane will generate self-signed certificates valid for 1<br />year without automatic certificate renewal.<br /> |


#### Transform







_Appears in:_
- [Validate](#validate)
- [ValueOrResolvedValue](#valueorresolvedvalue)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `from` _string_ | The value to transform. If `regex` is `true`, this is interpreted as<br />a regular expression that is matched against the input value.<br />Otherwise, this is interpreted as a literal string that is compared<br />fully to the input value. If the `from` value does not match the<br />input value, then this transformation has no effect. |  |  |
| `to` _string_ | The value to transform to. If `regex` is `true`, this may contain<br />references to capturing groups appearing in the `from` value,<br />otherwise it is just the literal output value. |  |  |
| `regex` _boolean_ | Whether to interpret `from` as a regular expression. |  |  |
| `global` _boolean_ | Whether to apply transformation to all matches of the regular<br />expression. If `global` is `true`, this transformation will be<br />applied to all occurrences of `from` within the current value. If<br />`global` is `false` or omitted, this transformation will be applied<br />to the first occurrence only. |  |  |
| `strategy` _[TransformStrategy](#transformstrategy)_ |  |  | Enum: [Compose ShortCircuit] <br /> |


#### TransformStrategy

_Underlying type:_ _string_

The strategy to use when chaining transformations.

- `Compose` indicates that the output value of the current transformation
should be applied as the input value to the next transformation.
- `ShortCircuit` indicates that all subsequent transformations should be
skipped if the current transformation matched on the input value.

If omitted, the default strategy is based on the `regex` value, with
`Compose` being used when `regex` is `true` and `ShortCircuit` being used
when `regex` is `false` or omitted.

_Validation:_
- Enum: [Compose ShortCircuit]

_Appears in:_
- [Transform](#transform)

| Field | Description |
| --- | --- |
| `Compose` |  |
| `ShortCircuit` |  |


#### TypedLocalObjectReference



TypedLocalObjectReference contains enough information to let you locate the
typed referenced object inside the same namespace.



_Appears in:_
- [CanaryRolloutTargetReference](#canaryrollouttargetreference)
- [QuotaEnforcementRecord](#quotaenforcementrecord)
- [ReleaseReference](#releasereference)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiGroup` _string_ | APIGroup is the group for the resource being referenced. |  |  |
| `kind` _string_ | Kind is the type of resource being referenced. |  |  |
| `name` _string_ | Name is the name of resource being referenced |  |  |


#### Validate







_Appears in:_
- [ProvisionUser](#provisionuser)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `jsonPath` _string_ | The JSONPath expression to use to resolve the value from the user<br />attributes in the external provider, which are assumed to be in JSON<br />format. |  |  |
| `required` _boolean_ | Whether the resolved value is required. | true |  |
| `transform` _[Transform](#transform) array_ | Transformations to apply to the value resolved by evaluating<br />`jsonPath` or to each element of the resolved array of values. If the<br />resolved value is not a value node (e.g. string, number) or an array<br />of value nodes, then `transform` is ignored. |  |  |
| `pattern` _string_ | If present, the regular expression that the resolved value must match. |  |  |
| `enum` _string array_ | If present, the set of values that the resolved value is constrained to. |  | MinItems: 1 <br /> |
| `items` _[ValidateString](#validatestring)_ | If present, the constraints to apply on all elements of the resolved<br />value, which must be an array of value nodes. |  |  |


#### ValidateEndpoint







_Appears in:_
- [CasSpec](#casspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `url` _string_ | The URL of the endpoint to use to validate service tickets. |  |  |


#### ValidateString







_Appears in:_
- [Validate](#validate)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `pattern` _string_ | If present, the regular expression that the resolved value must match. |  |  |
| `enum` _string array_ | If present, the set of values that the resolved value is constrained to. |  | MinItems: 1 <br /> |


#### ValueOrPath







_Appears in:_
- [ProvisionUser](#provisionuser)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `value` _string_ | If specified, the value to use. |  |  |
| `jsonPath` _string_ | If specified, the JSONPath expression to use to resolve the value<br />from the user attributes in the external provider, which are assumed<br />to be in JSON format. |  |  |


#### ValueOrResolvedValue







_Appears in:_
- [ProvisionUser](#provisionuser)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `value` _string_ | If specified, the value to use. |  |  |
| `jsonPath` _string_ | If specified, the JSONPath expression to use to resolve the value<br />from the user attributes in the external provider, which are assumed<br />to be in JSON format. |  |  |
| `transform` _[Transform](#transform) array_ | Transformations to apply to the value resolved by evaluating<br />`jsonPath` or to each element of the resolved array of values. If the<br />resolved value is not a value node (e.g. string, number) or an array<br />of value nodes, then `transform` is ignored. |  |  |


#### ValueOrSecretReference







_Appears in:_
- [OidcSpec](#oidcspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `value` _string_ | If specified, the value to use. |  |  |
| `secretRef` _[SecretReference](#secretreference)_ | If specified, the Secret resource reference to the value. |  |  |


#### ValueReference



ValueReference contains a reference to a resource containing values, and
optionally the key they can be found at



_Appears in:_
- [DatabaseSpec](#databasespec)
- [HelmAppSpec](#helmappspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `kind` _string_ | Kind of the values referent, valid values are ('Secret', 'ConfigMap'). |  | Enum: [Secret ConfigMap] <br /> |
| `name` _string_ | Name of the values referent. Should reside in the same namespace as the<br />referring resource. |  | MaxLength: 253 <br />MinLength: 1 <br /> |
| `dataKey` _string_ | DataKey is the data key where the a specific value can be<br />found at. Defaults to "data" | data |  |


#### WorkloadStatus



WorkloadStatus defines the observed state of a StatefulSet or a Deployment



_Appears in:_
- [DatabaseComponentsStatus](#databasecomponentsstatus)
- [DomainComponentsStatus](#domaincomponentsstatus)
- [HelmAppComponentsStatus](#helmappcomponentsstatus)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `name` _string_ | Name is the resource |  |  |
| `kind` _string_ | Kind is a string value representing the REST resource this object represents. |  |  |
| `version` _string_ | Version defines the schema version of this representation of an object. |  |  |
| `group` _string_ | Group defines the schema of this representation of an object. |  |  |
| `state` _string_ | The state of the resource |  |  |
| `message` _string_ | A human readable message indicating details about why the resource is in<br />this condition |  |  |
| `readyReplicas` _integer_ | ReadyReplicas is the number of pods created for this resource with a<br />Ready Condition. |  |  |
| `replicas` _integer_ | Replicas is the number of pods created by the resource controller. |  |  |


