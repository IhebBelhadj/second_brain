---
type: topic
created: 2026-09-26
tags: [topic]
---
# AWS

> What this covers: everything I'm learning about AWS. Services, how to click through them in the console, and above all **how they plug into each other**.

## Start here
1. [[AWS services overview]]: the big table of every service category, so I know what exists
2. [[How AWS services connect]]: follows one request from the browser to the database and shows which service does what along the way
3. Then dive into a domain below

## Networking (where things live)
- [[VPC]]: my private network. Subnets, route tables, internet gateway, NAT
- [[Connecting VPCs]]: peering vs transit gateway
- [[Proxies, load balancing and discovery in AWS]]: ALB, NLB, GWLB, CloudFront, API Gateway, Global Accelerator, Cloud Map, Service Connect, VPC Lattice, and egress control, mapped to the general concepts
- [[Site-to-Site VPN]]: the managed IPsec VPN. Customer gateway, virtual private gateway, two tunnels, static vs BGP, route propagation, CloudHub, limits (1.25 Gbps, 100 routes, MSS 1379) and the "tunnel UP but nothing works" checklist
- [[Transit gateway]]: the hub that replaces one VGW per VPC. Association vs propagation, segmentation, VPN ECMP, inspection VPC and appliance mode, peering, RAM, Connect attachments
- [[Direct Connect]]: a private physical link. Dedicated vs hosted, private/transit/public VIFs, Direct Connect gateway, VPN as backup, resilience, encryption, and what it takes to reach one instance over it
- [[Hybrid connectivity architectures]]: the problems in the order they show up (many VPCs, bandwidth, failover, overlap, DNS, a client network that's already a chain of VPNs, inspection, multi-region) and the design for each
- [[Connecting AWS to a private network]]: the managed VPN, and eight workarounds (EC2 as a VPN router, dial-out tunnels, mesh, SSH, connectors…) with where each one breaks
- [[Route 53]]: DNS, turns `myapp.com` into an address. Delegation from the registrar, Alias vs CNAME, private hosted zones (and the no-fallback trap), health checks and failover timing, routing policies combined, Resolver endpoints for hybrid DNS, DNSSEC and DNS Firewall
- [[Bastion host]]: how I get into servers sitting in a private subnet
- [[Security groups]]: the firewall on each resource, and how it differs from NACLs

## Storage (where my data lives)
- [[S3]]: object storage. Buckets and keys (no real folders), storage classes and lifecycle, versioning, replication, who can access a bucket, presigned URLs, gateway endpoints, and the 403s
- Not written yet: *[[EBS]]* (disks for EC2) · *[[EFS]]* (shared NFS)
- The vendor-neutral side (block/file/object, RAID, backups…) → [[Storage]]

## Databases (where my app's data lives)
- [[RDS]]: managed relational databases. What I give up (no SSH), Multi-AZ vs read replicas, failover through the endpoint, backups and point-in-time restore (always a new instance), RDS Proxy, Aurora, and the connection problems I'll debug

## Compute (what runs my code)
- [[EC2]]: virtual machines, launch templates
- [[Load balancers]]: ALB / NLB and **target groups**
- [[Auto Scaling]]: grows and shrinks the number of EC2 instances
- [[Lambda]]: run code without a server
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

## Security, identity & governance (who can do what)
- [[IAM]]: users, groups, roles, policies
- [[AWS Organizations]]: many accounts, SCPs
- [[AWS Identity Center]]: one login for many accounts
- [[Certificate Manager (ACM)]]: free HTTPS certificates
- [[Certificate rotation]]: keeping certificates renewed (ACME, ACM managed renewal, imported certs, CA rotation)
- [[AWS WAF]]: blocks bad HTTP requests
- [[CloudTrail]]: who did what, when
- [[ARN]]: how every resource gets its unique name
- [[AWS naming conventions]]: ID prefixes (`vpc-`, `sg-`…), naming rules, and my `project-env-resource` convention

## Related areas
- [[Networking]]: protocols behind all this (BGP, ICMP), routing, VPNs (IPsec/IKE), TLS
- [[Messaging]]: queues vs pub/sub vs logs, [[Kafka]], the concepts behind SQS/SNS/EventBridge
- [[Storage]]: block vs file vs object, filesystems, backups, the concepts behind S3/EBS/EFS

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
