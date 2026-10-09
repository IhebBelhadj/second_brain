---
type: subtopic
created: 2026-10-09
topic: AWS
tags: [subtopic, aws]
---
# AWS › Monitoring

> What this covers: is it working and how I operate it: CloudWatch, its agent, logs and alarms, Systems Manager.

Part of [[AWS]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[CloudWatch]]: metrics, namespaces and dimensions, retention, what EC2 doesn't show (memory, disk), custom namespaces with `PutMetricData` / EMF / StatsD, the high-cardinality trap, Metrics Insights and metric math, dashboards, and the whole "Insights" family
- [[CloudWatch agent]]: the agent inside the OS. IAM role, config JSON (custom namespace, append/aggregation dimensions, procstat, StatsD, log files), fleet rollout with Parameter Store and SSM, on-premises servers, private subnets, why metrics don't show up
- [[CloudWatch Logs]]: log groups and streams, retention, Logs Insights queries (errors per bin, p99, top customers, parse, Lambda REPORT), metric filters, subscription filters and cheap long-term archive, masking sensitive data
- [[CloudWatch alarms]]: states, M out of N, missing data, actions (SNS, Lambda, EC2 recover, scaling), alarming on symptoms with metric math and anomaly detection, page vs ticket, composite alarms and suppressors, auto-remediation, heartbeat alarms
- [[Systems Manager]]: the agent that dials out (why it works behind NAT with no inbound port → [[Outbound-initiated connections]]), managed node requirements, endpoints, Session Manager (shell, port forwarding to RDS, logging), Run Command with rate control, State Manager, Patch Manager, Parameter Store vs Secrets Manager, Automation runbooks, hybrid nodes, troubleshooting

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
