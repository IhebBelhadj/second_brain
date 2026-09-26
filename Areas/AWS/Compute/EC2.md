---
type: concept
created: 2026-09-20
topic: AWS
confidence: 2
tags: [aws, compute]
---
# EC2

> [!abstract] In one sentence
> A virtual machine (an **instance**) that I create from an image (**AMI**). It's where my code runs, and I'm in charge of everything on it.

## Creating an instance

![[Pasted image 20260920093658.png]]

To log into the instance from my machine (SSH), I need a **key pair**. AWS keeps the public key and I download the private one (`.pem`) **once**:

![[Pasted image 20260920093859.png]]

![[Pasted image 20260920094227.png]]

The **network settings** part of the form is where the instance meets the network:
- which [[VPC]] and which **subnet** it lives in (public or private)
- whether it gets a **public IP** (auto-assign)
- which **security group(s)** it wears

### Security groups
> A security group is a set of **firewall rules** attached to the instance (not the subnet). It says which traffic is allowed in and out.

- Only **allow** rules. Anything not allowed is blocked
- **Stateful**: if a request is allowed in, the response is automatically allowed back out
- The source of a rule can be an IP range **or another security group**. That's how "only the load balancer can reach my app" or "only the [[Bastion host]] can SSH in" are written
- Want `ping` to work? Allow **ICMP** (see [[ICMP]])
- Network ACLs are the subnet-level equivalent (see [[VPC]])

## Launch templates

> A saved "recipe" for an instance, so I don't click through the whole form every time. **[[Auto Scaling]] needs one** to know how to create new instances.

![[Pasted image 20260924191504.png]]

The creation form:
![[Pasted image 20260924191614.png]]

![[Pasted image 20260924192121.png]]

> [!note]
> The launch template form is basically the same form as launching an instance by hand. It just saves it instead of launching.

To use it: **Launch instance from template**:
![[Pasted image 20260924192453.png]]

## Target groups & load balancers
Target groups are part of load balancing, so they now have their own section in [[Load balancers]]. The one-line version: a target group is a list of instances that a load balancer can send traffic to, plus the health check used to decide which ones are OK.

## Connects to
- [[VPC]]: every instance lives in a subnet of a VPC
- [[Load balancers]]: instances are registered in target groups
- [[Auto Scaling]]: creates/destroys instances from a launch template
- [[IAM]]: an instance can get permissions through an **IAM role** (instance profile) instead of hardcoded keys
- [[Bastion host]]: how to reach instances in private subnets
- [[Route 53]]: point a domain at an Elastic IP
- [[Certificate Manager (ACM)]]: ACM certs can't go directly on an instance. Put an ALB in front
- [[Lightsail]]: simplified EC2. Lightsail snapshots can be exported to EC2
- Choosing → [[EC2 vs Lightsail vs Lambda]]
- Big picture → [[How AWS services connect]]

## Open questions

- [x] What is the difference between RSA and ED25519, and between OpenSSH and PuTTY?
  - **ED25519** is newer, with shorter keys, faster and considered more secure. **RSA** is older but supported everywhere, and it's **required for Windows instances**
  - **OpenSSH** (`.pem`) is the standard `ssh` client on Linux/macOS/modern Windows. **PuTTY** is an older Windows client that wants its own `.ppk` format. Today, `.pem` + the built-in `ssh` is enough
- [x] If my EC2 instance sits behind a private IP, how come I can SSH into it?
  - I can't directly. I go through a [[Bastion host]] (or Session Manager / EC2 Instance Connect Endpoint)

## Flashcards
#flashcards

What is an AMI? :: The image (OS + preinstalled software) an EC2 instance is created from
Is a security group attached to a subnet or an instance? :: An instance (its network interface). NACLs are the subnet-level firewall
Are security groups stateful? :: Yes, responses to allowed traffic are automatically allowed
What does Auto Scaling need to create instances? :: A launch template
How should an EC2 instance get AWS permissions? :: Through an IAM role (instance profile), never hardcoded access keys
