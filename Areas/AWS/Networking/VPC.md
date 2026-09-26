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
  - Every resource gets an ID with a prefix: `vpc-…`, `subnet-…`, `i-…` (instance), `sg-…`, `igw-…`, `nat-…`, `rtb-…`. The human name is just a **`Name` tag**. The globally unique name is the [[ARN]]
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
