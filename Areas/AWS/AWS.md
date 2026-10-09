---
type: topic
created: 2026-09-26
tags: [topic]
---
# AWS

> What this covers: everything I'm learning about AWS. Services, how to click through them in the console, and above all **how they plug into each other**.

## Sub-topics
Each sub-topic has its own index with the same reading order, for studying one part at a time (and a cleaner graph).
- [[AWS › Foundations]]: the ground rules: Regions and Availability Zones, ARNs (Amazon Resource Names), naming, the service map and how services connect
- [[AWS › Networking]]: every AWS networking note in 5 stages, with prerequisites and a question → note table
- [[AWS › Storage and databases]]: where data lives: S3, EFS, replication, RDS
- [[AWS › Compute]]: what runs my code: EC2, Auto Scaling, load balancers, Lambda, Lightsail, ECS, EKS, Packer
- [[AWS › Integration]]: services talking without waiting for each other: SQS, SNS, EventBridge, Step Functions
- [[AWS › Monitoring]]: is it working and how I operate it: CloudWatch, its agent, logs and alarms, Systems Manager
- [[AWS › Security]]: every AWS security, identity and audit note in 5 stages, with prerequisites and a question → note table

## Start here
1. [[AWS services overview]]: the big table of every service category, so I know what exists
2. [[How AWS services connect]]: follows one request from the browser to the database and shows which service does what along the way
3. [[AWS Regions and Availability Zones]]: choosing a Region, AZs (names vs IDs), global vs regional vs zonal resources, **opt-in Regions** and enabling them per account, enabled vs allowed (SCPs), STS tokens in opt-in Regions
4. Then dive into a domain below

## Networking (where things live)
Full reading path, prerequisites and a "which note answers…" table → [[AWS networking]]

**One VPC**
- [[VPC]]: my private network. Subnets, route tables, internet gateway, NAT
- [[Security groups]]: the firewall on each resource, and how it differs from NACLs
- [[VPC IP address planning]]: why every VPC CIDR should come from a plan. AWS rules (/16–/28, 5 reserved, no resizing), one block per environment, how it shrinks VPC/TGW/BGP/SG rules, a standard subnet layout, AWS IPAM pools, EKS pod ranges
- [[Bastion host]]: how I get into servers sitting in a private subnet

**Services inside AWS**
- [[Route 53]]: DNS, turns `myapp.com` into an address. Delegation from the registrar, Alias vs CNAME, private hosted zones (and the no-fallback trap), health checks and failover timing, routing policies combined, Resolver endpoints for hybrid DNS, DNSSEC and DNS Firewall
- [[Proxies, load balancing and discovery in AWS]]: ALB, NLB, GWLB, CloudFront, API Gateway, Global Accelerator, Cloud Map, Service Connect, VPC Lattice, and egress control, mapped to the general concepts

**Many VPCs**
- [[Connecting VPCs]]: peering vs transit gateway
- [[Transit gateway]]: the hub that replaces one VGW per VPC. Association vs propagation, segmentation, VPN ECMP, inspection VPC and appliance mode, peering, RAM, Connect attachments
- [[Transit gateway attachments]]: what an attachment is from a networking view (a managed interface, not a protocol), what each type runs underneath (VPC, VPN, DX, peering, Connect), MTU, why AWS designed the TGW around them, the router/VRF analogy
- [[Transit gateway routing]]: the two routing decisions (VPC table → TGW table), attach vs associate vs propagate, default tables, a packet traced from the office and back, static vs propagated, limiting propagation, short VPC routes

**AWS ↔ my network**
- [[Site-to-Site VPN]]: the managed IPsec VPN. Customer gateway, virtual private gateway, two tunnels, static vs BGP, route propagation, CloudHub, limits (1.25 Gbps, 100 routes, MSS 1379) and the "tunnel UP but nothing works" checklist
- [[BGP in AWS hybrid networking]]: BGP carries routes, not traffic. The chain office → BGP → VPN attachment → propagation → TGW table, what BGP never does (VPC routes), what AWS announces back, BGP vs propagation, segmentation still in TGW tables, failover between tunnels, static vs BGP, Direct Connect
- [[Direct Connect]]: a private physical link. Dedicated vs hosted, private/transit/public VIFs, Direct Connect gateway, VPN as backup, resilience, encryption, and what it takes to reach one instance over it
- [[Connecting AWS to a private network]]: the managed VPN, and eight workarounds (EC2 as a VPN router, dial-out tunnels, mesh, SSH, connectors…) with where each one breaks

**Designing it**
- [[Hybrid connectivity architectures]]: the problems in the order they show up (many VPCs, bandwidth, failover, overlap, DNS, a client network that's already a chain of VPNs, inspection, multi-region) and the design for each

## Storage (where my data lives)
- [[S3]]: object storage. Buckets and keys (no real folders), storage classes and lifecycle, versioning, replication, who can access a bucket, presigned URLs, gateway endpoints, and the 403s
- [[S3 replication]]: CRR/SRR step by step (versioning, role, rule), Batch Replication for existing objects, cross-account (bucket policy, ownership), **which account needs which Region enabled** (the exam question), SSE-KMS, deletes and Object Lock, RTC, two-way, what isn't replicated, PENDING/FAILED debugging
- [[EFS]]: managed NFS for **Linux** clients (not Windows: FSx). Mount targets per AZ and port 2049, the mount helper (`-t efs`, `tls`, `iam`) vs plain `nfs4`, IAM authorization with a file system policy, access points for apps and containers, storage classes and throughput modes, EFS vs EBS vs S3 vs FSx, mount failures
- Not written yet: *[[EBS]]* (disks for EC2)
- The vendor-neutral side (block/file/object, RAID, backups…) → [[Storage]]

## Databases (where my app's data lives)
- [[RDS]]: managed relational databases. What I give up (no SSH), Multi-AZ vs read replicas, failover through the endpoint, backups and point-in-time restore (always a new instance), RDS Proxy, Aurora, and the connection problems I'll debug

## Compute (what runs my code)
- [[EC2]]: virtual machines, launch templates
- [[Load balancers]]: ALB / NLB and **target groups**
- [[Auto Scaling]]: grows and shrinks the number of EC2 instances
- [[Packer]]: golden AMIs from code. Bake vs fry, immutable infrastructure, how an `amazon-ebs` build works, a full template, cleaning the image (no secrets, host keys, cloud-init), building through Session Manager, encrypted AMIs shared across accounts and regions (the KMS trap), a CI pipeline with Parameter Store and instance refresh, vs EC2 Image Builder
- [[Lambda]]: run code without a server
- [[ECS]]: AWS's container orchestrator. Cluster, task definition, task, service, capacity providers, ECR with immutable tags, the two IAM roles, a service behind an ALB (`ip` targets), the endpoints private tasks need to pull images, rolling deploys with circuit breaker, scaling, Service Connect, ECS Exec, why tasks stop
    - [[ECS tasks and task definitions]]: every field that matters, Fargate CPU/memory combinations, sidecars and `dependsOn`, how tasks get credentials, the task lifecycle, one-off/scheduled/orchestrated tasks (migrations, nightly jobs), stop codes and exit codes (137, 143)
    - [[ECS on Fargate vs EC2]]: serverless tasks vs provisioning container instances myself (ECS-optimized AMI, ecs.config, Auto Scaling group + capacity provider with managed scaling and draining, placement strategies, bridge vs awsvpc, IMDS trap, daemon services, AMI refresh), cost, and when to choose which
    - [[Kubernetes worked example on EKS]]: the Kubernetes shop moved to EKS with almost the same manifests. eksctl cluster (3-AZ VPC, managed node group, add-ons, Pod Identity), access entries, ECR, a Kustomize base + EKS overlay, StorageClass → EBS gp3, Ingress → ALB through the Load Balancer Controller (ACM, rule order), Secret from Secrets Manager via External Secrets, NetworkPolicies with the VPC CNI and the ALB, moving PostgreSQL to RDS, costs and the classic EKS failures
    - [[ECS production stack]]: the whole thing from a GitHub repo, prod ready. Terraform state and GitHub OIDC roles (no keys), 3-AZ VPC with endpoints, Route 53 zone + ACM DNS-validated cert, HTTPS ALB + WAF, ECS on an EC2 Auto Scaling group with capacity provider, Secrets Manager injection and rotation, ECR + task definition + service, GitHub Actions build-once/promote with migrations and approvals, alarms, and the Fargate alternative
- [[Lightsail]]: the "easy mode" VPS
- [[EC2 vs Lightsail vs Lambda]]: which one should I pick?

## Integration (how my services talk without waiting for each other)
- [[SQS]]: queues. Consumers pull and delete, visibility timeout and duplicates, dead-letter queues, standard vs FIFO (message groups), scaling workers on queue depth, Lambda batches
- [[SNS]]: pub/sub topics. One publish → every subscriber, fan-out to one SQS queue per consumer, filter policies, the envelope and raw delivery
- [[EventBridge]]: event buses and rules. Reacting to AWS's own events, routing my events by content, Scheduler, cross-account buses, archive and replay, Pipes
- [[SQS vs SNS vs EventBridge]]: which one (and which combination), plus when the answer is Kinesis, Amazon MQ or Step Functions instead
- [[Step Functions]]: serverless workflows. State types, Standard vs Express, the three ways a task waits (.sync, callback), Retry/Catch and sagas, Distributed Map over S3, a catalogue of architectures, and how it differs from Airflow
- [[Kafka vs AWS messaging services]]: Kafka (a replayable log) next to MSK, Kinesis, SQS, SNS and EventBridge, the exam keywords for each, and a design that combines them
- Not written yet: *[[Amazon MSK]]* · *[[Kinesis Data Streams]]*
- The vendor-neutral side (Kafka, delivery guarantees…) → [[Messaging]]

## Monitoring and operations (is it working, who changed what, how I operate servers)
- [[CloudWatch]]: metrics, namespaces and dimensions, retention, what EC2 doesn't show (memory, disk), custom namespaces with `PutMetricData` / EMF / StatsD, the high-cardinality trap, Metrics Insights and metric math, dashboards, and the whole "Insights" family
- [[CloudWatch agent]]: the agent inside the OS. IAM role, config JSON (custom namespace, append/aggregation dimensions, procstat, StatsD, log files), fleet rollout with Parameter Store and SSM, on-premises servers, private subnets, why metrics don't show up
- [[CloudWatch Logs]]: log groups and streams, retention, Logs Insights queries (errors per bin, p99, top customers, parse, Lambda REPORT), metric filters, subscription filters and cheap long-term archive, masking sensitive data
- [[CloudWatch alarms]]: states, M out of N, missing data, actions (SNS, Lambda, EC2 recover, scaling), alarming on symptoms with metric math and anomaly detection, page vs ticket, composite alarms and suppressors, auto-remediation, heartbeat alarms
- [[Systems Manager]]: the agent that dials out (why it works behind NAT with no inbound port → [[Outbound-initiated connections]]), managed node requirements, endpoints, Session Manager (shell, port forwarding to RDS, logging), Run Command with rate control, State Manager, Patch Manager, Parameter Store vs Secrets Manager, Automation runbooks, hybrid nodes, troubleshooting
- Audit of API calls → [[CloudTrail]] and [[CloudTrail in production]] (in Security below)

## Security, identity & governance (who can do what)
Full reading path in 5 stages, prerequisites, a "which note answers…" table and what's not written yet → [[AWS security]]

- [[IAM]]: users, groups, roles, policies. Console screens for creating policies, roles (trusted entity types), users and access keys
- [[STS]]: temporary credentials for roles. Why a role beats a user with the permissions, the two checks (identity policy + trust policy), what "trust this account" really means, external ID and confused deputy, GitHub OIDC with no stored keys, trusted entity types, what AssumeRole returns, debugging AccessDenied
    - [[Connecting GitHub Actions to AWS]]: production tutorial, no stored keys. OIDC provider per account, one role per job type (plan/build/deploy/infra) trusting an exact `sub`, the environment + branch rules that make approvals binding, least-privilege policies (Lambda, ECS, S3 site), Terraform bootstrap, ci/deploy workflows, hardening (SHA pins, pull_request_target, forks, custom sub), troubleshooting
    - [[Assuming a role step by step]]: the hands-on chain Lambda → invoke policy → role → assume-role policy → user with only that → access key → C#/Python/CLI client
- [[AWS Organizations]]: many accounts, SCPs
- [[AWS Identity Center]]: one login for many accounts
- [[Certificate Manager (ACM)]]: free HTTPS certificates
- [[Certificate rotation]]: keeping certificates renewed (ACME, ACM managed renewal, imported certs, CA rotation)
- [[AWS WAF]]: blocks bad HTTP requests
- [[CloudTrail]]: the audit log of API calls. Event anatomy, management vs data vs network activity events, org trail in a log archive account, advanced event selectors, log file validation, Insights, Athena vs Logs Insights (Lake closed to new customers)
- [[CloudTrail in production]]: alerting on dangerous calls (EventBridge rules, CIS metric filters), Athena investigations, playbooks: who deleted the database, assumed role → person, leaked access key, AccessDenied after a deploy, what changed before the outage, audit evidence
- [[ARN]]: how every resource gets its unique name
- [[AWS naming conventions]]: ID prefixes (`vpc-`, `sg-`…), naming rules, and my `project-env-resource` convention
- Not written yet: *[[Secrets Manager]]* · *[[KMS]]*

## Related areas
- [[Networking]]: protocols behind all this (BGP, ICMP), routing, VPNs (IPsec/IKE), TLS
- [[Messaging]]: queues vs pub/sub vs logs, [[Kafka]], the concepts behind SQS/SNS/EventBridge
- [[Storage]]: block vs file vs object, filesystems, backups, the concepts behind S3/EBS/EFS
- [[Containers]]: Docker images, tags and digests, the concepts behind ECS/ECR
- [[Identity and access]]: authentication methods, OAuth 2.0, OIDC, SSO, the concepts behind IAM, Identity Center and Cognito
- [[Infrastructure as code]]: building all of this with [[Terraform]], from the first apply to CI/CD pipelines and a full worked example

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE topic = this.file.name AND confidence
SORT confidence ASC
```

## Open questions
- What is **VPC Lattice** exactly? (came up in [[Auto Scaling]])
- ~~What is the transit gateway **Connect** attachment?~~ Answered in [[Transit gateway#Connect attachments: SD-WAN on top]]
- CloudFront doesn't have its own note yet, and it shows up in almost every architecture (S3 and RDS done → [[S3]], [[RDS]])
