---
type: concept
created: 2026-09-20
topic: AWS
confidence: 2
tags: [aws, networking]
---
# VPC

> [!abstract] In one sentence
> A VPC (Virtual Private Cloud) is **my own isolated network inside AWS**. Everything I launch (EC2, load balancers, databases…) lives in one of its subnets.

![[Pasted image 20260920090454.png]]

## What's inside a VPC

| Piece | Role |
|---|---|
| **VPC** | Defined by an IPv4 CIDR range (from /16 to /28), e.g. `10.0.0.0/16`. Can have extra CIDRs and IPv6 |
| **Subnets** | Slices of that range, each one in **one** Availability Zone |
| **Route tables** | Decide where traffic from a subnet goes |
| **Internet gateway (IGW)** | The VPC's door to the internet (one per VPC) |
| **NAT gateway** | Lets private subnets go *out* to the internet, but not be reached from it |
| **Security group** | Firewall at the **resource** level (see [[EC2]]) |
| <span style="color:rgb(192, 0, 0)">Network ACL</span> | Firewall at the **subnet** level (stateless, has allow *and* deny rules) |
| **Elastic IP** | A static public IPv4 address I keep until I release it |
| …more | These are only the important ones |

COLOR MAP (how well I know things):
- <span style="color:rgb(192, 0, 0)">Not learned yet</span>
- <span style="color:rgb(255, 192, 0)">Just a small encounter</span>
- <span style="color:rgb(146, 208, 80)">Mid knowledge</span>
- <span style="color:rgb(0, 112, 192)">Good grasp</span>
- Not sure

## Sub-services & features (full console menu)

> Everything this service contains, grouped the way the console's left menu groups it. Linked = I have a note on it.

The table above is the core. The full VPC console menu has much more:

| Menu group | Sub-service | What it's for |
|---|---|---|
| **Virtual private cloud** | Your VPCs | The VPCs themselves (+ the **VPC and more** wizard, see below) |
| | Subnets | Slices of the VPC, one AZ each |
| | Route tables | Where traffic goes |
| | Internet gateways | Door to the internet |
| | Egress-only internet gateways | Outbound-only door for **IPv6** (the IPv6 "NAT") |
| | Carrier gateways | For Wavelength zones (5G), which I'll probably never use |
| | DHCP option sets | Which DNS servers / domain name instances get |
| | Elastic IPs | Static public IPs |
| | Managed prefix lists | Named lists of CIDRs, reusable in route tables and security groups |
| | NAT gateways | Outbound internet for private subnets |
| | Peering connections | VPC ↔ VPC → [[Connecting VPCs]] |
| | Endpoints | Reach AWS services privately: **Gateway** (S3, DynamoDB, free) and **Interface** (PrivateLink, most services) |
| | Endpoint services | Expose *my* service to other VPCs via PrivateLink |
| **Security** | Network ACLs | Subnet-level firewall |
| | Security groups | Resource-level firewall |
| | Block Public Access | Account-wide switch to block internet access for VPCs |
| **DNS firewall** | Rule groups, domain lists | Block DNS lookups of bad domains from the VPC |
| **Network Firewall** | Firewalls, policies, rule groups | A managed stateful firewall / IDS in front of subnets |
| **Virtual private network** | Customer gateways, Virtual private gateways, Site-to-Site VPN connections | Encrypted tunnel to my office/data center |
| | Client VPN endpoints | Laptops connect into the VPC (like a company VPN) |
| **Transit gateways** | Transit gateways, attachments, route tables, policy tables, multicast | The hub → [[Connecting VPCs]] |
| **Traffic Mirroring** | Sessions, targets, filters | Copy network traffic to a monitoring appliance |
| **VPC Lattice** | Service networks, services, target groups | App-level service-to-service networking (still to study) |
| **Network analysis** | Reachability Analyzer | "Can A reach B? If not, which rule blocks it?" A great debugging tool |
| | Network Access Analyzer | Finds unintended network access paths |
| | IPAM | Plan and track IP ranges across accounts/regions |
| *(VPC → Actions)* | **Flow logs** | Log accepted/rejected traffic of a VPC/subnet/ENI to CloudWatch or S3 |

## Public vs private subnet

> [!important] There's no "public" checkbox
> A subnet is public or private **only because of its route table**:
> - **Public subnet** → its route table has `0.0.0.0/0 → internet gateway`
> - **Private subnet** → no route to the internet gateway (maybe `0.0.0.0/0 → NAT gateway` for outbound only)

The classic layout from the AWS docs, with public + private subnets, NAT gateway and internet gateway:

![[aws-docs vpc public private subnets nat.png]]

What typically goes where:
- **Public subnets**: [[Load balancers]], NAT gateway, [[Bastion host]]
- **Private subnets**: app servers ([[EC2]], [[Auto Scaling]] groups), databases, VPC-attached [[Lambda]]s

## Building it in the console

When creating a VPC, the first choice is **Resources to create**:
- **VPC only**: just the empty VPC. Then I build everything by hand (subnets, IGW, route tables, NAT…), which is what the sections below show step by step
- **VPC and more** ⭐: a wizard that builds the **whole network in one go** and shows a live preview of it

### The "VPC and more" wizard

![[Pasted image 20260926110144.png]]

The **Preview** on the right draws the whole thing (VPC → subnets → route tables → network connections), and it updates as I change options. Hovering a resource highlights everything it's linked to, which makes the preview a great way to *see* how the pieces connect.

The options, top to bottom:

| Option | What it does | What I'd pick |
|---|---|---|
| **Name tag auto-generation** | A prefix (`project`) used to auto-name every resource | The project name, e.g. `shop-prod` |
| **IPv4 CIDR block** | The VPC's IP range | `10.0.0.0/16` (65,536 IPs), which leaves room to grow |
| **IPv6 CIDR block** | None / Amazon-provided / my own | None, unless I need IPv6 |
| **Tenancy** | Default (shared hardware) or Dedicated | **Default**. Dedicated costs a lot more |
| **Number of Availability Zones** | 1, 2 or 3 | **2** minimum for high availability |
| **Number of public subnets** | 0, or one per AZ | One per AZ (for the ALB, NAT, bastion) |
| **Number of private subnets** | 0, one or two per AZ | One per AZ for apps, two per AZ if I want a separate DB layer |
| **Customize subnet CIDR blocks** | Change each subnet's range | Defaults are fine (`/20` each = 4,096 IPs) |
| **NAT gateways** | None / In 1 AZ / 1 per AZ | See below. **This one costs money** |
| **VPC endpoints** | None / S3 Gateway | **S3 Gateway**: free, lets private subnets reach S3 without a NAT |
| **DNS options** | Enable DNS hostnames / DNS resolution | Leave both **on** (needed for private hosted zones in [[Route 53]], VPC endpoints…) |

#### NAT gateway choice

| Option | Cost | Resilience |
|---|---|---|
| **None** | Free | Private subnets have **no internet** access at all |
| **In 1 AZ** | 1 NAT billed per hour + per GB | If that AZ goes down, private subnets in **every** AZ lose internet |
| **1 per AZ** | One NAT per AZ, so ×2 or ×3 the cost | Each AZ is independent. The production choice |

> [!warning] NAT gateways are billed **by the hour even when idle**
> For learning: choose **None** (or delete the NAT after the lab). Forgetting a NAT is a classic surprise on the bill.

#### What it creates (with the default 2 AZs / 2 public / 2 private)

From the name prefix `project` in region `eu-central-1`:

```
project-vpc                                   10.0.0.0/16
│
├── project-subnet-public1-eu-central-1a      10.0.0.0/20
├── project-subnet-public2-eu-central-1b      10.0.16.0/20
├── project-subnet-private1-eu-central-1a     10.0.128.0/20
├── project-subnet-private2-eu-central-1b     10.0.144.0/20
│
├── project-igw                               (attached to the VPC)
│
├── project-rtb-public                        0.0.0.0/0 → project-igw
│     └── shared by both public subnets
├── project-rtb-private1-eu-central-1a        (0.0.0.0/0 → NAT in 1a, if any)
├── project-rtb-private2-eu-central-1b        (0.0.0.0/0 → NAT in 1b, if any)
│
├── project-nat-public1-eu-central-1a         (only if NAT ≠ None, in a PUBLIC subnet)
└── project-vpce-s3                           (S3 gateway endpoint, added to private route tables)
```

Things to notice:
- **One public route table** for all public subnets, since they all go to the same IGW
- **One private route table per AZ**, because each AZ's private subnets should use **their own AZ's NAT**
- Public subnets are the lower half of the range and private ones start at `10.0.128.0`, which keeps them easy to tell apart
- The auto-names follow `<prefix>-<resource>-<detail>-<az>`, close to my own convention in [[AWS naming conventions]]

> [!tip] "VPC and more" vs building by hand
> The wizard is what I'd use in real life, because it's fast and hard to get wrong. Building by hand (below) is how I **learn** what each piece does. After the wizard, open each route table and check the routes. That's the best way to understand what it built.

> [!warning] Check **auto-assign public IPv4** on the public subnets
> The wizard doesn't necessarily turn it on. If instances in a "public" subnet get no public IP, enable it on the subnet (**Actions → Edit subnet settings**) or on the instance / launch template (see [[Auto Scaling]]).

### Internet gateway
> Creating an internet gateway only needs a name (tags optional).
> <span style="color:rgb(0, 112, 192)">IMPORTANT:</span> it does nothing until it's **attached to a VPC**.

![[Pasted image 20260920090600.png]]

![[Pasted image 20260920090821.png]]

### Subnets
> A subnet must be created **inside a VPC**, because its range has to fall inside the VPC's range. The **Add subnet** button lets me create several at once.

![[Pasted image 20260920091146.png]]

<span style="color:rgb(255, 192, 0); font-weight: bold">Availability Zone</span>: AZs are separate data centers inside a region, physically apart, so a flood or fire in one doesn't take down the others. Spreading subnets (and instances) over **at least two AZs** is how you survive that.

> [!warning]
> A subnet is associated with **exactly one** route table, but a route table can serve **many** subnets.

### Route tables

![[Pasted image 20260920092453.png]]

> Creating a route table only needs a name.
> ==The routes are added after creation==

![[Pasted image 20260920093146.png]]

<span style="color:rgb(255, 192, 0)">Subnet association</span>: this is where I link subnets to the route table:

![[Pasted image 20260920093403.png]]

### NAT gateway

**NAT gateway (Network Address Translation):** a managed resource that I put in a **public** subnet. It ==lets resources in private subnets make outbound connections to the internet without having public IPs.==

It swaps the private source IP for its own public IP and remembers the connection, so the replies come back to the right instance. Nobody on the internet can *start* a connection to the private resources.

When I need it: private servers downloading packages or updates, or calling external APIs. VPC-attached [[Lambda]]s need it too for internet access.

```
Private subnet route table:  0.0.0.0/0 → nat-xxxx
Public  subnet route table:  0.0.0.0/0 → igw-xxxx   (the NAT itself uses the IGW)
```

> [!note] Elastic IPs belong to the VPC world but are used by [[EC2]] instances and NAT gateways.

## Connects to
- [[EC2]]: instances live in subnets and wear security groups
- [[Load balancers]]: live in (public) subnets, across AZs
- [[Connecting VPCs]]: peering and transit gateways
- [[Bastion host]]: the door into private subnets
- [[Route 53]]: private hosted zones give internal DNS names inside the VPC
- [[Lambda]]: optional VPC attachment
- [[Lightsail]]: lives in a hidden AWS-managed VPC, which can be peered with my default VPC
- Big picture → [[How AWS services connect]]

## Open questions

- [x] How does a web server in a public subnet talk to a DB in a private subnet with its own route table?
  - Every route table in a VPC automatically has a **`local` route** for the whole VPC CIDR (`10.0.0.0/16 → local`). So **all subnets of the same VPC can always reach each other**, public or private. What actually controls it is the **security groups**: the DB's SG allows port 5432 from the web server's SG
- [x] What are the naming conventions for resources in AWS?
  - Every resource gets an ID with a prefix: `vpc-…`, `subnet-…`, `i-…` (instance), `sg-…`, `igw-…`, `nat-…`, `rtb-…`. The human name is just a **`Name` tag**. The globally unique name is the [[ARN]]. Full details and my convention → [[AWS naming conventions]]
- [ ] What are the norms for Availability Zones for disaster recovery?
  - Start: at least **2 AZs** for high availability (one AZ going down). **Another region** for real disaster recovery. To be studied: backup/restore → pilot light → warm standby → multi-site

## Flashcards
#flashcards

What makes a subnet public? :: Its route table has a route 0.0.0.0/0 to an internet gateway
What does a NAT gateway do? :: Lets private subnets make outbound internet connections without being reachable from the internet
Where does a NAT gateway live? :: In a public subnet
Security group vs NACL? :: Security group is per resource, stateful, allow rules only. NACL is per subnet, stateless, allow + deny
How many route tables can a subnet have? :: Exactly one (but a route table can have many subnets)
Can a public and a private subnet in the same VPC talk to each other? :: Yes, through the automatic `local` route. Security groups decide what's allowed
"VPC only" vs "VPC and more"? :: VPC only creates the empty VPC. VPC and more builds subnets, route tables, IGW, NAT and endpoints in one wizard
Why does "VPC and more" create one private route table per AZ? :: So each AZ's private subnets use the NAT gateway in their own AZ
NAT options in the wizard and the trade-off? :: None (free, no internet), 1 AZ (cheaper, single point of failure), 1 per AZ (resilient, costs more)
What does the S3 Gateway endpoint give private subnets? :: Access to S3 without a NAT gateway, for free
