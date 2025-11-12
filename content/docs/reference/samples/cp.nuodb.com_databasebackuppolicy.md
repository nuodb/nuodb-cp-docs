---
title: "DatabaseBackupPolicy"
description: "A sample DatabaseBackupPolicy object with fields documented"
summary: ""
draft: false
weight: 952
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
kind: DatabaseBackupPolicy
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-databasebackuppolicy
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the DatabaseBackupPolicy.
spec:
  # The backup execution frequency. Allowable values:
  # - Cron expression, e.g. `0 7 * * *`
  # - Predefined labels, e.g. `@hourly`, `@daily`, `@weekly`, `@monthly`, `@yearly`
  frequency: string
```

## Extended example

```yaml
# Standard Kubernetes API Version declaration.
apiVersion: cp.nuodb.com/v1beta1
# Standard Kubernetes Kind declaration.
kind: DatabaseBackupPolicy
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-databasebackuppolicy
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the DatabaseBackupPolicy.
spec:
  # The backup labels assignment rules. By default backup policy and database
  # labels are assigned to backups scheduled by this policy.
  backupLabelsAssignment:
    # Assign labels from matching database to backups created by this policy.
    fromDatabase: True
    # Assign labels from database backup policy to backups created by this
    # policy.
    fromPolicy: True
  # The backup execution frequency. Allowable values:
  # - Cron expression, e.g. `0 7 * * *`
  # - Predefined labels, e.g. `@hourly`, `@daily`, `@weekly`, `@monthly`, `@yearly`
  frequency: string
  # The backup plugin name managing this backup policy. Empty value means
  # that backups from this policy will be executed by the default backup
  # plugin if one is configured.
  pluginName: string
  # The number of retained artifacts for different frequencies. The number of
  # retained artifacts can only be specified for frequencies of the same or
  # lower granularity than the policy frequency. For example, if the policy
  # frequency is `@daily`, then retention can have values for `daily`,
  # `weekly`, `monthly` and `yearly`, but not for `hourly`. If the policy
  # frequency is `hourly`, then all retention values are allowed. If backup
  # retention is not defined, backups scheduled from this backup policy won't
  # be deleted automatically.
  retention:
    # Daily retention for backups.
    daily: 1
    # Hourly retention for backups.
    hourly: 1
    # Monthly retention for backups.
    monthly: 1
    # Additional backup rotation settings.
    settings:
      # The day of the week (Sunday = 0, ...) used to promote backup to weekly .
      # Weekly can be promoted from daily from any day of the week. For example,
      # the weekly backup may be chosen to be promoted from Sunday daily backups.
      # If a successful Sunday backup is not found due to a missed run or an
      # error, it will choose the next closest, such as a Saturday backup, and
      # treat that as weekly instead. Defaults to Sunday.
      dayOfWeek: 0
      # The month of the year (January = 1, ...) used to promote backup to
      # yearly. Yearlies can be promoted from any month of the year, such as
      # January, December, or the company’s fiscal year-end. Defaults to January.
      monthOfYear: 1
      # Whether to promote the latest backup within the day if multiple backups
      # exist for that day. By default the first successful backup from the day
      # is retained.
      promoteLatestToDaily: False
      # Whether to promote the latest backup within the hour if multiple backups
      # exist for that hour. By default the first successful backup from the hour
      # is retained.
      promoteLatestToHourly: False
      # Whether to promote the latest backup within the month if multiple backups
      # exist for that month. By default the first successful backup from the
      # month is retained.
      promoteLatestToMonthly: False
      # Whether to apply the backup rotation scheme relative to the last
      # successful backup instead to the current time. This allows older backups
      # for the configured number of periods to be retained in case the policy is
      # suspended or latest backups are failing. Enabled by default.
      relativeToLast: True
    # Weekly retention for backups.
    weekly: 1
    # Yearly retention for backups.
    yearly: 1
  # A label query over resources for which the backup policy is applied. It
  # must match the resource labels. More info:
  # https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors
  selector:
    # matchExpressions is a list of label selector requirements. The requirements are ANDed.
    matchExpressions:
    -
      # key is the label key that the selector applies to.
      key: string
      # operator represents a key's relationship to a set of values.
      # Valid operators are In, NotIn, Exists and DoesNotExist.
      operator: string
      # values is an array of string values. If the operator is In or NotIn,
      # the values array must be non-empty. If the operator is Exists or DoesNotExist,
      # the values array must be empty. This array is replaced during a strategic
      # merge patch.
      values:
      - string
    # matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels
    # map is equivalent to an element of matchExpressions, whose key field is "key", the
    # operator is "In", and the values array contains only "value". The requirements are ANDed.
    matchLabels:
      {}
  # Optional deadline in seconds for starting the policy if the scheduled
  # time is missed for any reason.
  startingDeadlineSeconds: 1
  # Suspended disables the backup policy temporary so that no backups are
  # scheduled from it.
  suspended: true
# Current observed status of the DatabaseBackupPolicy.
status:
  # Conditions holds the conditions for the DatabaseBackupPolicy.
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
  # Last database backups that were not scheduled by this policy.
  lastMissedBackups:
  -
    # The database name for which a backup was missed.
    database: string
    # A human readable message indicating details about the missed backup.
    message: string
    # The time that a backup was missed.
    missedTime: 2025-11-11T21:30:40.971508Z
    # A programmatic identifier indicating the reason for missing a backup.
    reason: string
  # The last time when a database backup was not scheduled by this policy on
  # time and was missed due to controller downtime or clock skew.
  lastMissedScheduleTime: 2025-11-11T21:30:40.971508Z
  # The last time when database backups were successfully scheduled by this
  # policy.
  lastScheduleTime: 2025-11-11T21:30:40.971508Z
  # The next time for database backups to be scheduled by this policy.
  nextScheduleTime: 2025-11-11T21:30:40.971508Z
```
