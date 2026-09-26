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
- [[Route 53]]: DNS, turns `myapp.com` into an address
- [[Bastion host]]: how I get into servers sitting in a private subnet

## Compute (what runs my code)
- [[EC2]]: virtual machines, launch templates, security groups
- [[Load balancers]]: ALB / NLB and **target groups**
- [[Auto Scaling]]: grows and shrinks the number of EC2 instances
- [[Lambda]]: run code without a server
- [[Lightsail]]: the "easy mode" VPS
- [[EC2 vs Lightsail vs Lambda]]: which one should I pick?

## Security, identity & governance (who can do what)
- [[IAM]]: users, groups, roles, policies
- [[AWS Organizations]]: many accounts, SCPs
- [[AWS Identity Center]]: one login for many accounts
- [[Certificate Manager (ACM)]]: free HTTPS certificates
- [[AWS WAF]]: blocks bad HTTP requests
- [[CloudTrail]]: who did what, when
- [[ARN]]: how every resource gets its unique name

## Related areas
- [[Networking]]: protocols behind all this (BGP, ICMP)

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE topic = this.file.name AND confidence
SORT confidence ASC
```

## Open questions
- What is **VPC Lattice** exactly? (came up in [[Auto Scaling]])
- What is the transit gateway **Connect** attachment? (came up in [[Connecting VPCs]])
- CloudFront, RDS and S3 don't have their own notes yet, and they show up in almost every architecture
