---
type: concept
created: 2026-09-26
topic: AWS
confidence: 1
tags: [aws, networking, security]
---
# Bastion host

> [!abstract] In one sentence
> A small EC2 instance in a **public** subnet that is the only door into my **private** subnets: I SSH into the bastion first, then "jump" from it to the private servers.

## The problem it solves

This answers my open question from [[EC2]]: *"If my EC2 instance sits behind a private IP, how can I SSH into it?"*

→ **Directly, I can't.** A private subnet has no route to the internet gateway (see [[VPC]]), so nothing from the internet can reach it. That's the whole point. But I still need to get in to debug.

So I put one well-guarded machine at the edge:

```
                        ┌──────────────────── VPC 10.0.0.0/16 ────────────────────┐
                        │                                                          │
                        │   Public subnet 10.0.1.0/24     Private subnet 10.0.2.0/24│
                        │   (route → IGW)                 (no route → IGW)          │
  Me (laptop)           │  ┌──────────────┐              ┌──────────────┐          │
  IP 41.x.x.x ──SSH:22──┼─►│ Bastion host │───SSH:22────►│  App server  │          │
                   IGW  │  │ public IP    │              │  10.0.2.15   │          │
                        │  └──────────────┘              └──────────────┘          │
                        └──────────────────────────────────────────────────────────┘
```

## The security groups are the important part

| Security group | Inbound rule | Why |
|---|---|---|
| `bastion-sg` | SSH (22) from **my IP only** (`41.x.x.x/32`) | Not `0.0.0.0/0`! The whole internet would be knocking |
| `private-app-sg` | SSH (22) from **source = `bastion-sg`** | "Anything wearing the bastion's security group". No IPs to maintain |

> [!tip] Security group referencing
> A rule's source can be **another security group** instead of an IP range. That's how "only the bastion can SSH in" is written. The same trick is used for "only the ALB can reach my app" and "only the app can reach the DB".

## How to do it

1. Launch a small [[EC2]] instance (`t3.micro` is enough) in the **public subnet**, with **auto-assign public IP** on, and `bastion-sg`
2. Private instances get `private-app-sg`
3. From my laptop, jump through it in **one command**:

```bash
ssh -i mykey.pem -J ec2-user@<bastion-public-ip> ec2-user@10.0.2.15
```

Or once and for all in `~/.ssh/config`:
```
Host bastion
    HostName <bastion-public-ip>
    User ec2-user
    IdentityFile ~/.ssh/mykey.pem

Host app
    HostName 10.0.2.15
    User ec2-user
    IdentityFile ~/.ssh/mykey.pem
    ProxyJump bastion
```
→ then just `ssh app`

> [!warning] Never copy my private key (`.pem`) onto the bastion
> If the bastion gets compromised, so does every server. `-J` / `ProxyJump` (or agent forwarding) keeps the key on my laptop.

## Modern alternatives (no bastion at all)

The bastion is the classic answer and shows up in exams, but AWS now has options with **no public door at all**:

| Option | How it works | Needs |
|---|---|---|
| **Session Manager** (Systems Manager) | Shell in the browser/CLI through the SSM agent. **No port 22 open, no keys** | SSM agent (pre-installed on Amazon Linux), an [[IAM]] role on the instance, a route to SSM (NAT or VPC endpoints) |
| **EC2 Instance Connect Endpoint** | An endpoint inside my VPC that tunnels SSH/RDP to private instances | Creating the endpoint in a subnet + security group rules |

EC2 Instance Connect Endpoint, from the AWS docs:

![[aws-docs ec2 instance connect endpoint.png]]

Bonus: both are logged (Session Manager can record full sessions, and the API calls show up in [[CloudTrail]]). A bastion only logs what I set up myself.

## Connects to
- [[VPC]]: public vs private subnets, route tables, internet gateway
- [[EC2]]: key pairs, security groups, the instances I'm reaching
- [[IAM]]: roles for Session Manager
- [[CloudTrail]]: auditing who connected
- [[Lightsail]]: doesn't need this. Lightsail instances are public, with browser SSH
- Big picture → [[How AWS services connect]]

## Easy to get wrong
- Opening 22 to `0.0.0.0/0` on the bastion
- Putting the bastion in the **private** subnet (then I can't reach it either 🙃)
- Forgetting that the bastion needs a **public IP** (auto-assign or Elastic IP)
- Private instances allowing SSH from the whole VPC CIDR instead of just the bastion's SG
- A bastion is a single point of entry, so patch it and keep it tiny

## Flashcards
#flashcards

What is a bastion host? :: A hardened instance in a public subnet used as the only SSH entry point into private subnets
Inbound rule for the bastion's security group? :: SSH (22) from my IP only, not 0.0.0.0/0
Inbound rule for private instances? :: SSH (22) with the bastion's security group as the source
SSH through a bastion without copying the key? :: `ssh -J user@bastion user@private-ip` (ProxyJump)
Two ways to reach private instances without a bastion? :: SSM Session Manager and EC2 Instance Connect Endpoint

## Links
- [EC2 Instance Connect Endpoint (docs)](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connect-with-ec2-instance-connect-endpoint.html)
- [Session Manager (docs)](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html)
