---
title: "Backup policies"
description: ""
summary: ""
date: 2024-09-24T14:22:10+03:00
lastmod: 2024-09-24T14:22:10+03:00
draft: false
weight: 333
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

Database backup policies automate backup creation and backup retention as part of an enterprise's data protection strategy.
Policies define rules that give users granular control over database backups, enabling them to achieve the desired recovery point objective (RPO).

## Frequency

Each policy defines the schedule at which regular backups are taken using [Cron format](https://crontab.guru/)

{{< callout context="caution" title="Caution" icon="outline/alert-triangle" >}}
Multiple policies with the same or overlapping frequencies matching the same database will try to schedule backups simultaneously.
Only one of the backups will succeed and the other will be reported as _missed_.
For more information on missed backups, see [List missed backups by policy]({{< ref "#list-missed-backups-by-policy" >}})
{{< /callout >}}

## Targets selection

A single backup policy matches one or multiple target databases.
Target databases are matched by defining _scope_, SLA, service tier, and user labels.
The target selection is an intersection among all filters.

The scope has the format `<organization>/<project>/<database>` which binds to a specific object in the hierarchy of NuoDBaaS objects (_organizations_, _projects_, _databases_) and expands to the set of databases to backup.
For example, the scope `acme/messaging` selects all databases within _acme_ organization and _messaging_ project.
Policies created in one organization may select databases in different organizations as long as the user has sufficient access privileges to define a policy with a scope wider than a single organization.

## Backup retention

NuoDBaaS enforces the configured retention for regular backups to meet the RPO.
By default, all backups are retained indefinitely, however, you can define high-level rules for keeping only certain backups.

### Backup rotation scheme

The Grandfather-father-son (GFS) backup scheme is a data retention strategy designed to protect critical data through a hierarchical data backup method.
GFS backup rotation happens cyclically, with each backup occurring at the scheduled time repeatedly.
Users configure the number of backups to retain from each cycle.

The available cycles are `hourly`, `daily`, `weekly`, `monthly`, and `yearly`.
For example, `7 daily` means that up to seven daily backups with the last seven days will be retained.
A _daily_ backup is any completed backup requested during the same day.
The period for different cycles can overlap to increase the backup coverage.

#### Example

The diagrams below illustrate an example retention configuration and the backups that are retained for different cycles.
User configured backup policy to retain 3 _daily_, 4 _weekly_, 6 _montly_ and 2 _yearly_ backups.
Assuming that today is July 18th, 2024, the retained backups from the last year are shown below.

- Daily backups in <span style="color:#f19e38">orange</span>
- Weekly backups in <span style="color:#54808c">blue</span>
- Monthly backups in <span style="color:#8b1a10">red</span>
- Yearly backups in <span style="color:#78a65a">green</span>

{{< picture src="retention-example.png" alt="Backup retention example" >}}

By default, weekly backups are chosen on Sunday, monthly on the first day of the month, and yearly on the first day of the year.
The backup rotation scheme is fine-tuned based on the user's preferences using the `retention.settings` backup policy field.

As time passes, new backups for each cycle are retained and those outside of the time range are deleted.
For example, once a daily backup is taken on July 19th, the one from July 16th will be automatically deleted.
By default, the rotation scheme is applied relative to the last successful backup, if any.

{{< callout context="tip" title="Retain a backup" icon="outline/info-circle" >}}
To prevent a specific backup from being deleted by the backup rotation scheme and keep it forever, add a special label to the backup object with the key `keep-forever` and value `true`.
{{< /callout >}}

### Create a backup policy

Create a backup policy that schedules backups every day for all databases in organization `acme`, and project `messaging`.

{{< tabs "create-policy" >}}
{{< tab "nuodb-cp" >}}

```sh
nuodb-cp backuppolicy create acme/messagingdaily \
 --frequency '@daily' \
  --selector-scope acme/messaging \
 --daily-retention 3 \
  --weekly-retention 4 \
 --monthly-retention 6 \
  --yearly-retention 2
```

{{< /tab >}}
{{< tab "curl" >}}

```sh
curl -X PUT -H 'Content-Type: application/json' \
 $NUODB_CP_URL_BASE/backuppolicies/acme/messagingdaily \
    -d '{"frequency": "@daily", "selector": {"scope": "acme/messaging"}, "retention": {"daily": 3, "weekly": 4, "monthly": 6, "yearly": 2}}'
```

{{< /tab >}}
{{< tab "terraform" >}}

```terraform
resource "nuodbaas_backuppolicy" "pol" {
 organization = "acme"
 name         = "messagingdaily"
 frequency = "@daily"
 selector = {
 scope = "acme/messaging"
 }
 retention = {
 daily   = 3
 weekly  = 4
 monthly = 6
 yearly  = 2
 }
}
```

{{< /tab >}}
{{< /tabs >}}

### List databases for a policy

List all the databases that a policy matches.

{{< tabs "policy-list-databases" >}}
{{< tab "nuodb-cp" >}}

```sh
nuodb-cp backuppolicy list-databases acme/messagingdaily
```

{{< /tab >}}
{{< tab "curl" >}}

```sh
curl -X GET -H 'Content-Type: application/json' \
 $NUODB_CP_URL_BASE/backuppolicies/acme/messagingdaily/databases
```

{{< /tab >}}
{{< /tabs >}}

### List backups for a policy

List all the backups scheduled by a backup policy.

{{< tabs "policy-list-backups" >}}
{{< tab "nuodb-cp" >}}

```sh
nuodb-cp backuppolicy list-backups acme/messagingdaily
```

{{< /tab >}}
{{< tab "curl" >}}

```sh
curl -X GET -H 'Content-Type: application/json' \
 $NUODB_CP_URL_BASE/backuppolicies/acme/messagingdaily/backups
```

{{< /tab >}}
{{< /tabs >}}

### List missed backups by policy

In certain cases, it might not be possible for a policy to schedule a backup on time
For example:
- The NuoDBaaS operator is not running
- The target database is disabled
- A backup for this database was taken at the same time

List all missed backups for the policy from the last schedule that had missed backups.

{{< tabs "policy-list-missed" >}}
{{< tab "nuodb-cp" >}}

```sh
nuodb-cp backuppolicy get acme/messagingdaily | jq '.status.lastMissedBackups'
```

{{< /tab >}}
{{< tab "curl" >}}

```sh
curl -X GET -H 'Content-Type: application/json' \
 $NUODB_CP_URL_BASE/backuppolicies/acme/messagingdaily | jq '.status.lastMissedBackups'
```

{{< /tab >}}
{{< /tabs >}}

Example output:

```json
[
 {
    "missedTime": "2024-10-09T12:00:00Z",
    "database": "acme/messaging/demo",
    "reason": "DatabaseDisabled",
    "message": "database is disabled"
 }
]
```

### Suspend and resume a policy

A backup policy can be temporarily suspended, ensuring no new backups are scheduled.
Edit the `suspended` field to suspend or resume a backup policy.

{{< callout context="note" title="Note" icon="outline/info-circle" >}}
Backups from a suspended policy are not recorded as missed backups.
{{< /callout >}}
