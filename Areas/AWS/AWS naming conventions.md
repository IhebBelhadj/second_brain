---
type: concept
created: 2026-09-26
topic: AWS
confidence: 1
tags: [aws]
---
# AWS naming conventions

> [!abstract] In one sentence
> Every AWS resource has **three kinds of names**: an **ID** that AWS generates (`vpc-0a1b…`), an **[[ARN]]** that is unique across AWS, and a **human name** that I choose (usually the `Name` tag). Only the human name is up to me, so pick a convention and stick to it.

## 1. IDs that AWS generates (the prefixes)

I don't choose these, but recognizing the prefix tells me instantly what I'm looking at in a route table, a log or an error:

| Prefix | Resource | Note |
|---|---|---|
| `vpc-` | [[VPC]] | |
| `subnet-` | Subnet | |
| `igw-` | Internet gateway | |
| `nat-` | NAT gateway | |
| `rtb-` | Route table | |
| `acl-` | Network ACL | |
| `sg-` | Security group | |
| `eni-` | Network interface | |
| `eipalloc-` | Elastic IP (allocation) | |
| `pcx-` | VPC peering connection | [[Connecting VPCs]] |
| `tgw-` / `tgw-attach-` | Transit gateway / attachment | [[Connecting VPCs]] |
| `vpce-` | VPC endpoint | |
| `i-` | [[EC2]] instance | |
| `ami-` | AMI (image) | |
| `vol-` | EBS volume | |
| `snap-` | EBS snapshot | |
| `lt-` | Launch template | |
| `key-` | Key pair | |

Load balancers, target groups and Auto Scaling groups have **no short ID**. They're identified by **the name I give them** + their ARN:
```
arn:aws:elasticloadbalancing:eu-west-1:123456789012:loadbalancer/app/shop-prod-alb/50dc6c495c0c9188
arn:aws:elasticloadbalancing:eu-west-1:123456789012:targetgroup/shop-prod-tg-web/73e2d6bc24d8a067
```
And an ALB's DNS name is built from its name: `shop-prod-alb-1234567890.eu-west-1.elb.amazonaws.com` (internal ALBs start with `internal-`).

## 2. Rules AWS enforces on names

| Resource | Rules |
|---|---|
| **Load balancer** (ALB/NLB) | Max **32** chars, letters/digits/hyphens, can't start or end with `-`, can't start with `internal-`. **Can't be renamed** |
| **Target group** | Max **32** chars, letters/digits/hyphens. Can't be renamed |
| **Auto Scaling group** | Up to 255 chars, **can't be renamed** |
| **Launch template** | 3–128 chars |
| **Security group** | Up to 255 chars, **can't start with `sg-`**, can't be renamed (only the `Name` tag can change) |
| **S3 bucket** | 3–63 chars, **lowercase**, digits, hyphens/dots, **globally unique across all AWS accounts** |
| **IAM user / role** | Up to 64 chars, unique in the account |
| **Tags** | Key ≤ 128 chars, value ≤ 256 chars, max 50 tags per resource, `aws:` prefix is reserved |
| VPC, subnet, IGW, NAT, route table, EC2… | No real name, just a **`Name` tag** that can be changed any time |

> [!warning] The 32-character limit on ALBs and target groups
> A long convention like `mycompany-production-application-load-balancer` won't fit. Keep the parts short (`prod`, not `production`).

## 3. A convention for the human names

AWS doesn't impose one. This is the common pattern I'll use:

```
<project>-<env>-<resource>-<detail>
```
- all **lowercase**, words separated by **hyphens**
- env: `dev` / `stg` / `prod`
- detail: role (`web`, `api`, `db`), visibility (`public`/`private`), AZ (`a`, `b`)

Example for a project called `shop` in production:

| Resource | Name |
|---|---|
| VPC | `shop-prod-vpc` |
| Subnets | `shop-prod-subnet-public-a`, `shop-prod-subnet-public-b`, `shop-prod-subnet-private-a`… |
| Internet gateway | `shop-prod-igw` |
| NAT gateway | `shop-prod-nat-a` (one per AZ) |
| Route tables | `shop-prod-rtb-public`, `shop-prod-rtb-private-a` |
| Security groups | `shop-prod-sg-alb`, `shop-prod-sg-web`, `shop-prod-sg-db`, `shop-prod-sg-bastion` |
| Load balancer | `shop-prod-alb` |
| Target group | `shop-prod-tg-web` |
| Launch template | `shop-prod-lt-web` |
| Auto Scaling group | `shop-prod-asg-web` |
| EC2 instance (`Name` tag) | `shop-prod-web` (ASG instances share it) / `shop-prod-bastion` |
| Key pair | `shop-prod-key` |
| IAM role | `shop-prod-ec2-web-role`, `shop-prod-lambda-resize-role` |
| Lambda | `shop-prod-resize-images` |
| S3 bucket | `shop-prod-uploads-123456789012` (account ID for global uniqueness) |

Why it pays off:
- Route tables and security group rules show **IDs**. With a clear `Name` tag, the console shows what `sg-0a1b…` actually is
- Filtering the console by `shop-prod` shows everything that belongs to one app
- Sorting keeps related things together

## 4. Tags beyond `Name`

Tags are key/value labels on resources. A basic set to put on everything:

| Tag | Example | Why |
|---|---|---|
| `Name` | `shop-prod-web` | What the console displays |
| `Project` | `shop` | Group resources by app |
| `Environment` | `prod` | Separate dev/prod, use in IAM conditions |
| `Owner` | `iheb` | Who to ask before deleting it |
| `CostCenter` | `team-a` | Split the bill (activate as **cost allocation tags** in Billing) |

- Tags on a **launch template** / ASG can be propagated to the instances it creates
- IAM policies can use tags: "devs can only stop instances with `Environment=dev`"
- [[AWS Organizations]] **tag policies** can enforce the convention across accounts

## Connects to
- [[ARN]]: the globally unique name
- [[VPC]], [[EC2]], [[Load balancers]], [[Auto Scaling]]: the resources being named
- [[IAM]]: tag-based permissions
- [[AWS Organizations]]: tag policies

## Flashcards
#flashcards

What is `rtb-0a1b2c`? :: A route table ID
What is `pcx-…`? :: A VPC peering connection
What is `eni-…`? :: A network interface
Max length of an ALB or target group name? :: 32 characters
Can you rename a load balancer or a security group? :: No, only recreate it (a security group's Name tag can change)
Where does the "name" of a VPC or subnet actually live? :: In its `Name` tag
Why add the account ID to an S3 bucket name? :: Bucket names must be globally unique across all AWS accounts
A good naming pattern? :: `<project>-<env>-<resource>-<detail>`, lowercase with hyphens, e.g. `shop-prod-sg-web`

## Links
- [Tagging best practices (AWS whitepaper)](https://docs.aws.amazon.com/whitepapers/latest/tagging-best-practices/tagging-best-practices.html)
- [ALB naming rules](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/create-application-load-balancer.html)
- [S3 bucket naming rules](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html)
