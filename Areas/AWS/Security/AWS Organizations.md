---
type: concept
created: 2026-09-20
topic: AWS
confidence: 2
tags: [aws, security, governance]
---
# AWS Organizations

> [!abstract] In one sentence
> **AWS Organizations** lets me manage **many AWS accounts as one**: group them, pay one bill, and apply guardrails (SCPs) to all of them at once.

Instead of 20 AWS accounts managed separately, they all go under one organization, with central policies, billing and governance.

> [!question] Why do I need this if IAM already manages users?
> Because IAM works **inside one account**, and Organizations works **across accounts**. An account is much more than a user (see below). Companies split things into many accounts (prod, dev, security, one per team…), and IAM alone can't govern them all consistently.

## Sub-services & features

> Everything this service contains, grouped the way the console's left menu groups it. Linked = I have a note on it.

| Menu | Sub-feature | What it's for |
|---|---|---|
| **AWS accounts** | Root, OUs, accounts | The tree: create/invite/move/close accounts |
| **Invitations** | | Invite existing accounts to join |
| **Policies** | **Service control policies (SCPs)** | Cap what **principals** in accounts can do (see below) |
| | **Resource control policies (RCPs)** | Cap what can be done **to resources** (e.g. no S3 access from outside the org) |
| | **Declarative policies** | Enforce service settings (e.g. EC2: block public AMI sharing, require IMDSv2) |
| | Tag policies | Enforce tag keys/values → [[AWS naming conventions]] |
| | Backup policies | Org-wide AWS Backup plans |
| | AI services opt-out policies | Opt out of AWS using data to improve AI services |
| | Chat applications policies | Control access from Slack/Teams (Amazon Q Developer) |
| **Services** | Trusted access | Let services work org-wide: [[CloudTrail]] org trail, [[AWS Identity Center\|Identity Center]], Config, GuardDuty, Security Hub… |
| | Delegated administrator | Let a member account (e.g. Security) manage a service instead of the management account |
| **Settings** | | Org ID, feature set (**all features** vs consolidated billing only) |
| *(Billing)* | Consolidated billing | One bill, volume discounts shared across accounts |

## The hierarchy

```
                 AWS Organization
                        │
                ┌───────┴────────┐
                │                │
          Production OU      Development OU
                │                │
          ┌─────┴─────┐     ┌────┴─────┐
          │           │     │          │
       Prod A      Prod B  Dev A     Dev B
       Account     Account Account   Account
          │           │     │          │
        IAM         IAM   IAM        IAM
          │           │     │          │
       Users &     Users & Users &  Users &
       Roles       Roles   Roles    Roles
```

An **Organizational Unit (OU)** is just a folder for accounts. OUs can be nested:

```
Organization
│
└── Workloads
    │
    ├── Production
    │   ├── Europe
    │   └── US
    │
    └── NonProduction
        ├── Development
        └── Staging
```

## SCPs: the guardrails

> An **SCP (Service Control Policy)** defines the **maximum permissions** available in the member accounts.
> <span style="color:rgb(255, 192, 0)">Important: an SCP does <b>not grant</b> anything.</span>
> - <span style="color:rgb(0, 112, 192)">IAM policy → grants permissions</span>
> - <span style="color:rgb(0, 112, 192)">SCP → limits the maximum permissions</span>

```
IAM permissions
        ∩
SCP permissions
        =
Effective permissions
```

**Concrete example**: this SCP is on the account:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Action": "ec2:TerminateInstances",
      "Resource": "*"
    }
  ]
}
```
and I create an admin role in that account with:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ec2:*",
      "Resource": "*"
    }
  ]
}
```
The IAM policy says "all of EC2", but the SCP says "never terminate". **Result: the admin can do everything on EC2 except terminate instances.**

What Organizations gives me overall:
```
                  AWS Organizations
                         │
       ┌─────────────────┼──────────────────┐
       ▼                 ▼                  ▼
      SCPs        Consolidated billing   Account management
       │
       ▼
   Governance
```

### When this comes in handy

SCPs shine when I want to <span style="color:rgb(255, 192, 0)">deny something for a whole group of accounts</span>.

Example: *nobody in any of our 50 accounts can use `ap-southeast-1`.*

**With only IAM**, I'd have to put the restriction in the policies of **every** account, and hope nobody removes it:
```
Account 1 → IAM policy
Account 2 → IAM policy
...
Account 50 → IAM policy
```

**With Organizations + SCP**, once, on the OU:
```
                   Organization
                        │
                   Workloads OU  ◄── SCP: Deny ap-southeast-1
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
    Account A       Account B       Account C
```

## User vs account

An account contains many users:
```
                AWS Account
              ┌───────────────────────┐
              │   IAM                 │
              │   ├── Alice           │
              │   ├── Bob             │
              │   └── AdminRole       │
              │                       │
              │   AWS Resources       │
              │   ├── EC2             │
              │   ├── S3              │
              │   └── RDS             │
              └───────────────────────┘
```

An **account** is a whole container. It has its own:
- account ID
- billing boundary
- [[IAM]] configuration
- AWS resources, in every region
- security and admin boundary

### <span style="color:rgb(255, 192, 0)">Can one person access several accounts?</span>

**Old way**: one IAM user per account (3 passwords, 3 sets of keys…):
```
Production Account  └── IAM User: Alice
Development Account └── IAM User: Alice
Security Account    └── IAM User: Alice
```

**Modern way**: <span style="color:rgb(255, 192, 0)">IAM Identity Center</span> (see [[AWS Identity Center]]). One identity, many accounts:
```
                 IAM Identity Center
                         │
                       Alice
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
       Production    Development   Security
         Account       Account     Account
             │           │           │
          ReadOnly      Admin       No access
```

```
Alice → Identity Center → assumes a role in Production → uses AWS resources
```

## Control Tower vs Organizations

**Control Tower** is an opinionated, ready-made **multi-account setup** built *on top of* Organizations (landing zone, pre-made guardrails, log archive account…):
```
              Control Tower
                    │
                    ▼
             AWS Organizations
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
      OUs          SCPs      Accounts
```

## Quick summary

| Component | Responsibility | Example |
|---|---|---|
| **OU** | Groups accounts | Production accounts |
| **SCP** | Caps the max permissions of accounts | Block EC2 termination |
| **IAM** | Permissions inside one account | Alice can read S3 |
| **IAM Identity Center** | Gives people access to accounts | Alice gets ReadOnly in Production |

## In the console

Inside the organization I see all my **OUs**:
![[Pasted image 20260920205439.png]]

Creating an OU only needs a name (tags optional):
![[Pasted image 20260920205530.png]]

> Inside OUs I can put other OUs or AWS accounts. Here's the form for creating a new account directly from the organization:

![[Pasted image 20260920205624.png]]

## Connects to
- [[IAM]]: SCPs cap what IAM policies can grant
- [[AWS Identity Center]]: people access across the org's accounts
- [[CloudTrail]]: an **organization trail** logs every account in one place
- [[Connecting VPCs]]: transit gateways are often shared across the org's accounts
- Big picture → [[How AWS services connect]]

## Flashcards
#flashcards

Does an SCP grant permissions? :: No, it only limits the maximum. IAM grants
Effective permissions with Organizations? :: The intersection of IAM permissions and SCP permissions
What is an OU? :: An organizational unit, a folder of accounts (can be nested) that policies attach to
Control Tower vs Organizations? :: Control Tower is a ready-made, governed multi-account setup built on top of Organizations
How should one person access several accounts today? :: IAM Identity Center: one identity, a role per account
