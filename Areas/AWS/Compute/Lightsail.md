---
type: concept
created: 2026-09-26
topic: AWS
confidence: 1
tags: [aws, compute]
---
# Lightsail

> [!abstract] In one sentence
> The "easy mode" of AWS: a virtual server with disk, bandwidth and a static IP bundled together for a **fixed monthly price**, managed from its own simple console.

## In my own words

Launching a website on [[EC2]] "properly" means doing: [[VPC]] → subnets → route table → internet gateway → security group → key pair → EC2 → Elastic IP → [[Route 53]] → maybe a load balancer + [[Certificate Manager (ACM)|ACM]]…

Lightsail hides all of that. I pick a plan (like "2 GB RAM, 2 vCPU, 60 GB SSD"), pick a **blueprint** (plain Ubuntu, or pre-installed WordPress / LAMP / Node.js…), and I have a running server with a fixed price.

Under the hood **it is EC2**, running in a VPC that AWS manages for me and that I can't see.

## Lightsail's mini-world

Lightsail has its own simplified versions of the "real" services:

| In Lightsail | The "real AWS" equivalent |
|---|---|
| Instance | [[EC2]] instance |
| Firewall (per instance) | Security group |
| Static IP (free while attached) | Elastic IP |
| DNS zone | [[Route 53]] hosted zone |
| Load balancer (+ free certificate) | [[Load balancers\|ALB]] + [[Certificate Manager (ACM)\|ACM]] |
| Managed database | RDS |
| Bucket | S3 |
| Distribution | CloudFront |
| Container service | ECS / App Runner |
| Snapshot | AMI / EBS snapshot |

## Console walkthrough (screenshots from the AWS docs)

1. **Lightsail console → Create instance**

![[aws-docs lightsail create instance.png]]

2. Pick a **region and Availability Zone**, then a platform (Linux/Windows) and a **blueprint**, then a plan:

![[aws-docs lightsail region and AZ.png]]

3. Once it's running, the instance page has everything in tabs: Connect, Metrics, Snapshots, Storage, **Networking**, Domains…

![[aws-docs lightsail instance tabs.png]]

4. **Connect**: SSH straight from the browser, no key pair juggling:

![[aws-docs lightsail connect ssh.png]]

![[aws-docs lightsail browser terminal.png]]

5. **Networking tab → firewall**. The same idea as a security group, just simpler (and IPv4 and IPv6 rules are separate):

![[aws-docs lightsail firewall.png]]

6. **Networking tab → attach a static IP**. Otherwise the public IP changes when the instance stops/starts:

![[aws-docs lightsail static ip.png]]

7. **Domains & DNS → create a DNS zone**, then copy its name servers to my registrar (exactly like a Route 53 hosted zone):

![[aws-docs lightsail dns zone.png]]

## How Lightsail links to the rest of AWS 🔗

### 1. Outgrowing Lightsail → move to EC2
Take a snapshot → **Export to Amazon EC2**:

![[aws-docs lightsail export snapshot.png]]

This creates an **AMI + EBS snapshot** on the EC2 side. From there Lightsail even offers a "Create EC2 instance" page that finds the closest instance type:

![[aws-docs lightsail to ec2 ami details.png]]

![[aws-docs lightsail to ec2 compute.png]]

```
Lightsail instance → snapshot → export → AMI in EC2 → EC2 instance
                                                     → launch template → Auto Scaling
```
(One-way trip: there's no "import from EC2 into Lightsail")

### 2. Talking to resources in my VPC → VPC peering
Lightsail lives in its own hidden VPC. To reach, say, an RDS database in my **default** VPC, I enable **VPC peering** in the account settings (one checkbox per region):

![[aws-docs lightsail vpc peering.png]]

Same idea as the peering in [[Connecting VPCs]], but AWS does it for me. Limitation: only with the **default VPC** of the same region.

### 3. DNS
Either Lightsail's own DNS zones (free, simple) or [[Route 53]] with an A record to the Lightsail static IP.

## When to use it, when not to

✅ Good for:
- A blog, portfolio, small business site, WordPress
- Dev/test boxes, learning Linux
- When I want a **predictable bill** (a few dollars a month for the small plans)

❌ Move to EC2 when I need:
- [[Auto Scaling]] (Lightsail has no auto scaling)
- Custom VPC design: private subnets, NAT, [[Bastion host]]s, transit gateways
- Lots of instance types, GPUs, Spot instances
- IAM roles attached to instances, deep integration with other services

More in [[EC2 vs Lightsail vs Lambda]].

## Easy to get wrong
- A Lightsail firewall is **not** a security group, and they don't show up in the EC2 console
- The monthly price includes a **data transfer allowance**. Going over costs extra
- Stopped instances **still cost** money (the disk and IP are still reserved). Delete them to stop paying
- VPC peering only works with the **default** VPC

## Flashcards
#flashcards

What is Lightsail? :: A simplified VPS service: an instance + SSD + data transfer + static IP for a fixed monthly price
How do you move a Lightsail instance to EC2? :: Create a snapshot → Export to Amazon EC2 → it becomes an AMI → launch an EC2 instance from it
How can a Lightsail instance reach an RDS database in my AWS account? :: Enable VPC peering (Lightsail ↔ default VPC of the same region)
What is the Lightsail equivalent of a security group? :: The instance firewall (Networking tab)
Name one reason to move from Lightsail to EC2 :: Auto scaling, custom VPC networking, more instance types, IAM roles on instances

## Links
- [Lightsail getting started (docs, lots of screenshots)](https://docs.aws.amazon.com/lightsail/latest/userguide/getting-started.html)
- [Quick start: WordPress](https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-quick-start-guide-wordpress.html)
- [Export snapshots to EC2](https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-exporting-snapshots-to-amazon-ec2.html)
- [VPC peering](https://docs.aws.amazon.com/lightsail/latest/userguide/lightsail-how-to-set-up-vpc-peering-with-aws-resources.html)
