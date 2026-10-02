# Area guide: AWS

**Index:** `AWS.md` lists every note by domain with a one-line summary, plus open questions. Read it for *what* a note covers; use this file for *where* it is.

**Scope:** AWS services for the current certification: console walkthroughs, how services plug together, exam traps. General concepts (how NAT, DNS, load balancing, VPNs work) belong in `Areas/Networking/`. AWS notes link to them instead of re-explaining, and "concept → AWS product" mappings live here.

## Folder map

```
AWS/
├── AWS.md                          topic index
├── AWS services overview.md        every service category (type: note)
├── How AWS services connect.md     one request from browser to database, service by service
├── ARN.md                          resource names
├── AWS naming conventions.md       ID prefixes, naming rules, project-env-resource convention
├── Compute/
│   ├── EC2.md                      instances, launch templates
│   ├── Load balancers.md           ALB/NLB setup, target groups, health checks
│   ├── Auto Scaling.md             scaling groups
│   ├── Lambda.md                   serverless functions
│   ├── Lightsail.md                simple VPS
│   └── EC2 vs Lightsail vs Lambda.md   which to pick
├── Networking/
│   ├── VPC.md                      subnets, route tables, internet/NAT gateways, console wizard
│   ├── Security groups.md          stateful per-interface firewall vs NACLs
│   ├── Connecting VPCs.md          peering vs transit gateway, transitivity
│   ├── Connecting AWS to a private network.md   managed VPN + 8 workarounds and their limits
│   ├── Proxies, load balancing and discovery in AWS.md   ALB/NLB/GWLB/CloudFront/API GW/GA/Cloud Map/Lattice, egress control
│   ├── Route 53.md                 hosted zones, records, routing policies, resolver
│   └── Bastion host.md             reaching private instances
├── Databases/
│   └── RDS.md                      Multi-AZ vs replicas, backups/PITR, RDS Proxy, Aurora, connection debugging
├── Storage/
│   └── S3.md                       buckets, storage classes, lifecycle, versioning, replication, access, endpoints (also indexed in Storage)
└── Security/
    ├── IAM.md                      users, roles, policies
    ├── AWS Organizations.md        accounts, SCPs
    ├── AWS Identity Center.md      SSO across accounts
    ├── Certificate Manager (ACM).md   certificates
    ├── Certificate rotation.md     ACME, ACM renewal, CA rotation (also indexed in Networking)
    ├── AWS WAF.md                  L7 filtering, comparison with SGs/NACLs/Network Firewall/Shield
    └── CloudTrail.md               audit log
```

Many notes embed console screenshots from `Attachments/` (`![[aws-console … sidebar.png]]`, `![[aws-docs … .png]]`). Keep those embeds when editing.

## Where a new note goes

| It's about… | Folder |
|---|---|
| Something that runs code (ECS, EKS, Batch) | `Compute/` |
| Networking services (CloudFront, Direct Connect, Global Accelerator) | `Networking/` |
| Identity, encryption, audit, protection (KMS, Secrets Manager, Shield, GuardDuty) | `Security/` |
| Storage (EBS, EFS, AWS Backup) | `Storage/` (also add it to section 7 of `Areas/Storage/Storage.md`) |
| Databases (DynamoDB, ElastiCache) | `Databases/` |
| Cross-cutting (pricing, Well-Architected, exam strategy) | Area root |

`AWS.md` → "Open questions" lists gaps the owner has noticed (e.g. no CloudFront note yet).
