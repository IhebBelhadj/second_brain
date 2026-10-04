# Area guide: AWS

**Index:** `AWS.md` lists every note by domain with a one-line summary, plus open questions. Read it for *what* a note covers; use this file for *where* it is.

**Sub-indexes:**
- `Networking/AWS networking.md` is the networking reading path (5 stages, the Networking notes to read first, a "which note answers…" table, planned notes). A new networking note goes in **both** `AWS.md` (same stage group) and `AWS networking.md`.
- `Security/AWS security.md` is the security reading path (5 stages: IAM/STS, keyless machines and pipelines, many accounts, traffic protection, audit; the Identity and access / Networking notes to read first; a "which note answers…" table; planned notes). A new security note goes in **both** `AWS.md` and `AWS security.md` (replace its italic planned link if there is one).

**Scope:** AWS services for the current certification: console walkthroughs, how services plug together, exam traps. General concepts (how NAT, DNS, load balancing, VPNs work) belong in `Areas/Networking/`. AWS notes link to them instead of re-explaining, and "concept → AWS product" mappings live here.

## Folder map

```
AWS/
├── AWS.md                          topic index
├── AWS services overview.md        every service category (type: note)
├── How AWS services connect.md     one request from browser to database, service by service
├── ARN.md                          resource names
├── AWS naming conventions.md       ID prefixes, naming rules, project-env-resource convention
├── AWS Regions and Availability Zones.md   Regions, AZ names vs IDs, global/regional/zonal, opt-in Regions, enabling per account, SCP region guardrails
├── Compute/
│   ├── EC2.md                      instances, launch templates
│   ├── Load balancers.md           ALB/NLB setup, target groups, health checks
│   ├── Auto Scaling.md             scaling groups
│   ├── Packer.md                   golden AMIs from code, bake vs fry, template, cleanup, SSM builds, sharing/KMS, pipeline, vs Image Builder
│   ├── Lambda.md                   serverless functions
│   ├── ECS.md                      containers: cluster/task def/task/service, ECR, roles, ALB, endpoints, deploys, scaling, Exec, troubleshooting
│   ├── ECS tasks and task definitions.md   fields, Fargate sizes, sidecars, credentials, lifecycle, run-task/scheduled tasks, stop/exit codes
│   ├── ECS on Fargate vs EC2.md    (compare) Fargate vs self-provisioned container instances: capacity providers, placement, network modes, cost
│   ├── ECS production stack.md     end to end from GitHub: Terraform/OIDC, VPC, Route 53 + ACM, ALB/WAF, ECS on EC2, secrets, CI/CD, alarms, Fargate alternative
│   ├── Lightsail.md                simple VPS
│   └── EC2 vs Lightsail vs Lambda.md   which to pick
├── Networking/
│   ├── AWS networking.md           sub-index: reading order in 5 stages, prerequisites, question → note table, roadmap
│   ├── VPC.md                      subnets, route tables, internet/NAT gateways, console wizard
│   ├── Security groups.md          stateful per-interface firewall vs NACLs
│   ├── Connecting VPCs.md          peering vs transit gateway, transitivity
│   ├── Site-to-Site VPN.md         customer gateway, VGW, two tunnels, static vs BGP, propagation, CloudHub, limits, troubleshooting
│   ├── Transit gateway.md          hub for VPNs/VPCs, association vs propagation, segmentation, ECMP, inspection, Connect
│   ├── VPC IP address planning.md  org-wide CIDR plan, routing payoff, subnet layout, IPAM pools, pod ranges
│   ├── BGP in AWS hybrid networking.md   BGP vs propagation, route chain to TGW, what each side announces, tunnel failover, static vs BGP
│   ├── Transit gateway attachments.md   what attachments are, per-type data/control plane, design reasons, VRF analogy, lifecycle
│   ├── Transit gateway routing.md  two-stage routing, attach/associate/propagate, defaults, packet trace, limiting propagation
│   ├── Direct Connect.md           physical link, VIF types, DX gateway, VPN backup, resilience, encryption, reaching an instance
│   ├── Hybrid connectivity architectures.md   problems → designs: many VPCs, bandwidth, HA, overlap, DNS, chained client VPNs
│   ├── Connecting AWS to a private network.md   managed VPN + 8 workarounds and their limits
│   ├── Proxies, load balancing and discovery in AWS.md   ALB/NLB/GWLB/CloudFront/API GW/GA/Cloud Map/Lattice, egress control
│   ├── Route 53.md                 hosted zones, Alias, private zones, health checks/failover, routing policies, Resolver endpoints, DNSSEC
│   └── Bastion host.md             reaching private instances
├── Databases/
│   └── RDS.md                      Multi-AZ vs replicas, backups/PITR, RDS Proxy, Aurora, connection debugging
├── Integration/
│   ├── SQS.md                      queues, visibility timeout, DLQ, standard vs FIFO, scaling consumers
│   ├── SNS.md                      pub/sub topics, fan-out to SQS, filter policies, subscriber types
│   ├── EventBridge.md              buses, rules/patterns, AWS service events, Scheduler, archive/replay, Pipes
│   ├── Step Functions.md           state machines, Standard vs Express, integration patterns, sagas, Distributed Map, architectures, vs Airflow
│   ├── SQS vs SNS vs EventBridge.md   which to pick, common exam patterns
│   └── Kafka vs AWS messaging services.md   Kafka vs MSK/Kinesis/SQS/SNS/EventBridge (also indexed in Messaging)
├── Storage/
│   ├── S3.md                       buckets, storage classes, lifecycle, versioning, replication, access, endpoints (also indexed in Storage)
│   ├── S3 replication.md           CRR/SRR setup, Batch Replication, cross-account, Region enablement rules, KMS, deletes, RTC, troubleshooting (also indexed in Storage)
│   └── EFS.md                      managed NFS (Linux only), mount targets, mount helper, IAM/file system policy, access points, classes, vs FSx (also indexed in Storage)
├── Monitoring/
│   ├── CloudWatch.md               metrics, custom namespaces (PutMetricData/EMF), dimensions, retention, Metrics Insights, dashboards, Insights family
│   ├── CloudWatch agent.md         install, IAM, config JSON, fleet rollout via SSM, on-prem, private subnets, troubleshooting
│   ├── CloudWatch Logs.md          log groups, retention, Logs Insights queries, metric/subscription filters, archive to S3
│   ├── CloudWatch alarms.md        states, M of N, missing data, actions, symptom alerting, composite alarms, remediation
│   └── Systems Manager.md          agent dial-out model, endpoints, Session Manager, Run Command, State/Patch Manager, Parameter Store, Automation
└── Security/
    ├── AWS security.md             sub-index: reading order in 5 stages, prerequisites, question → note table, roadmap
    ├── IAM.md                      users, roles, policies
    ├── STS.md                      temporary credentials, AssumeRole, trust policies, external ID, GitHub OIDC, why roles over users
    ├── Connecting GitHub Actions to AWS.md   (procedure) production GitHub OIDC: provider, per-job roles, environments, Terraform, workflows, hardening
    ├── Assuming a role step by step.md   (procedure) console + code: outside app invokes a Lambda via a user that can only assume a role
    ├── AWS Organizations.md        accounts, SCPs
    ├── AWS Identity Center.md      SSO across accounts
    ├── Certificate Manager (ACM).md   certificates
    ├── Certificate rotation.md     ACME, ACM renewal, CA rotation (also indexed in Networking)
    ├── AWS WAF.md                  L7 filtering, comparison with SGs/NACLs/Network Firewall/Shield
    ├── CloudTrail.md               audit log: events, event types, org trail, selectors, validation, Insights, querying
    └── CloudTrail in production.md   alerts (EventBridge, metric filters), Athena investigations, incident playbooks, audit evidence
```

Many notes embed console screenshots from `Attachments/` (`![[aws-console … sidebar.png]]`, `![[aws-docs … .png]]`). Keep those embeds when editing.

## Where a new note goes

| It's about… | Folder |
|---|---|
| Something that runs code (ECS, EKS, Batch) | `Compute/` |
| Networking services (CloudFront, PrivateLink, Network Firewall, Client VPN) | `Networking/` (also add it to `Networking/AWS networking.md`, and replace its italic planned link if there is one) |
| Identity, encryption, audit, protection (KMS, Secrets Manager, Shield, GuardDuty) | `Security/` (also add it to `Security/AWS security.md`, and replace its italic planned link if there is one) |
| Monitoring and operations (CloudWatch, X-Ray, Config, Systems Manager) | `Monitoring/` |
| Storage (EBS, EFS, AWS Backup) | `Storage/` (also add it to section 7 of `Areas/Storage/Storage.md`) |
| Databases (DynamoDB, ElastiCache) | `Databases/` |
| Messaging and workflows (Kinesis, MSK, Step Functions, Amazon MQ) | `Integration/` (also add it to section 5 of `Areas/Messaging/Messaging.md`) |
| Cross-cutting (pricing, Well-Architected, exam strategy) | Area root |

`AWS.md` → "Open questions" lists gaps the owner has noticed (e.g. no CloudFront note yet).
