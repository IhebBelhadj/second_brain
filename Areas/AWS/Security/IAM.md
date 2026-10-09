---
type: concept
created: 2026-09-20
topic: AWS
subtopic: AWS › Security
confidence: 2
tags: [aws, security]
---
# IAM

> [!abstract] In one sentence
> IAM (**Identity and Access Management**) decides **who** (a user, or a service like EC2/Lambda) can do **what** on **which** resources inside one AWS account.

## Sub-services & features

> Everything this service contains, grouped the way the console's left menu groups it. Linked = I have a note on it.

![[aws-console iam sidebar.png|250]]

| Menu group | Sub-service | What it's for |
|---|---|---|
| **Dashboard** | | Security recommendations (MFA on root, etc.) |
| **Access management** | User groups | Groups of users sharing policies |
| | Users | People/apps with long-term credentials. Per user: console password, **MFA**, **access keys**, **Access Advisor** (last accessed) |
| | Roles | Identities assumed temporarily (EC2, Lambda, cross-account, SSO) |
| | Policies | AWS-managed + my own (customer-managed) policies |
| | Identity providers | Trust an external login (SAML / OIDC, e.g. GitHub Actions, Google) |
| | Account settings | Password policy, STS regions |
| | Root access management | Centrally manage/remove root credentials of member accounts (with [[AWS Organizations\|Organizations]]) |
| **Access reports** | **Access Analyzer** | Finds resources shared **outside** my account, **unused** permissions, and validates/generates policies |
| | Credential report | CSV of every user + password/key age and MFA status |
| | Organization activity | Last-accessed info at the org level |
| | Service control policies | Read-only view of SCPs (managed in Organizations) |

Policy types to know: **identity-based** (on users/groups/roles), **resource-based** (on the resource, e.g. S3 bucket policy, Lambda policy), **permissions boundaries** (cap for a user/role), **SCPs/RCPs** (cap for accounts, from Organizations), **session policies**.

## Root user vs IAM users

The first time I log into AWS, I'm the **root user** (the email I signed up with). Root can do *everything*, including closing the account. So:
- use root only to create the first admin IAM user and for the rare root-only tasks
- turn on MFA on root, and then put it away

![[Pasted image 20260920193211.png]]

## The building blocks

| Piece | What it is |
|---|---|
| **User** | A person (or an old-school app) with long-term credentials: password and/or access keys |
| **Group** | A bag of users. Attach policies to the group, not to each user |
| **Role** | An identity with **no password**, *assumed* temporarily by someone or something (EC2, Lambda, another account, SSO users) |
| **Policy** | A JSON (JavaScript Object Notation) document: which **actions** are **allowed/denied** on which **resources** |
| **Trust policy** | The special policy on a **role** that says *who may assume it*. Assuming happens through [[STS]] (Security Token Service) |

> A policy is just an access grant on a resource, and it can be very granular: e.g. "can read items but not create them".

The IAM console:

![[Pasted image 20260920193711.png]]

### Users and groups

When creating a user, I can add it to a group or attach permissions directly. In real life: **put permissions on groups** and put users in groups. It's much easier to manage than 50 users with 50 custom policy sets.
![[Pasted image 20260920193901.png]]

The *Set permissions* step has three options: **Add user to group**, **Copy permissions** (all groups and policies of an existing user), or **Attach policies directly**. Attaching directly is acceptable for a single technical user with one narrow policy, like a program that may only assume one role ([[Assuming a role step by step]]):

![[Pasted image 20261004102620.png]]

A user's page: the ARN, whether console access is enabled, its two access key slots, and the tabs. **Security credentials** holds the console password, MFA (Multi-Factor Authentication) devices and access keys:

![[Pasted image 20261004102725.png]]

> [!note] Every resource I create gets a unique identifier, its <span style="color:rgb(255, 192, 0)">ARN</span> (**Amazon Resource Name**). More in [[ARN]].

![[Pasted image 20260920194115.png]]

To let the user log into the console, enable **console access** in the *Security credentials* tab.

The group view:
![[Pasted image 20260920201941.png]]

### Creating policies

![[Pasted image 20260920201531.png]]

Either the **visual editor** or raw **JSON**:

![[Pasted image 20260920193547.png]]

In the visual editor, I pick a **service**, then the **actions** grouped by access level (List, Read, Write, Permissions management, Tagging), then the **resources** (*Specific* ARNs or *All*), then optional **request conditions**. Here, Lambda: `InvokeFunction` sits under *Write*.

![[Pasted image 20261004100435.png]]

The review page summarizes the policy per service: access level (*Limited: Write* = some write actions, not all) and the resources it's scoped to. Reading it is a quick check that I didn't grant *Full* or *All resources* by accident:

![[Pasted image 20261004100525.png]]

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}
```

How AWS evaluates:
1. By default everything is **denied**
2. An explicit **Allow** opens it
3. An explicit **Deny** always wins over any Allow

### Roles: how services get permissions

A role has two policies: a **permissions** policy (what it can do) and a **trust** policy (who may assume it). Whoever assumes it gets **temporary credentials** from [[STS]]. Why that beats giving a user the permissions, and how GitHub, other accounts and SSO (Single Sign-On) users assume roles, is all in [[STS]].

This is how the services in my other notes get their rights, **without storing keys anywhere**:

| Who | Role | Example |
|---|---|---|
| [[EC2]] instance | Instance profile | The app on the instance reads from S3 |
| [[Lambda]] function | Execution role | The function writes logs, reads a DynamoDB table |
| [[Bastion host]] replacement | Instance role with SSM permissions | Session Manager access with no SSH |
| SSO user | Permission set → role | [[AWS Identity Center]] users assume a role in each account |

### Creating a role

IAM → Roles → **Create role** is three steps.

**1. Select trusted entity**: who may assume the role. The type decides the trust policy the console writes (details per type in [[STS#Stage 7: the same idea everywhere in AWS]]):

![[Pasted image 20261004101523.png]]

- **AWS service**: EC2 (Elastic Compute Cloud), Lambda, ECS (Elastic Container Service) tasks…, the service assumes it for my code
- **AWS account**: this account or another one. Option: **Require external ID** for third parties
- **Web identity**: an OIDC (OpenID Connect) provider like GitHub Actions, or Cognito
- **SAML 2.0 federation** (SAML = Security Assertion Markup Language): a corporate directory
- **Custom trust policy**: write the JSON myself

**2. Add permissions**: attach the permissions policies (my own customer-managed ones appear next to the AWS-managed ones):

![[Pasted image 20261004101852.png]]

**3. Name, review, and create**: the console shows the **trust policy** it generated. For *This account* with an external ID:

![[Pasted image 20261004101920.png]]

The role page. The things I come back for: the **role ARN** (what callers assume), the **maximum session duration** (1 hour by default, up to 12), the **link to switch roles** in the console, and the tabs *Permissions*, **Trust relationships** (edit who may assume), *Access Advisor* and **Revoke sessions** (invalidate every session issued so far):

![[Pasted image 20261004102014.png]]

### Access keys

An **access key** is a user's long-term credential for the API (Application Programming Interface), CLI (Command Line Interface) and SDKs (Software Development Kits): a key ID starting with `AKIA` and a secret. Each user can have **two** (so one can be rotated while the other still works).

Security credentials → **Create access key** first asks what it's for, and for most answers recommends something better than a key: CloudShell or [[AWS Identity Center|Identity Center]] for the CLI, a **role** for code running on EC2/ECS/Lambda. A key is accepted for an application running **outside** AWS (or a third-party service), with the rules: never in plain text, a code repository or code, disable when unused, least privilege, rotate.

![[Pasted image 20261004102841.png]]

The secret is shown **once**. Download the CSV (Comma-Separated Values) file or copy it now, otherwise the only fix is a new key:

![[Pasted image 20261004103108.png]]

> [!tip] A key that can only assume a role
> When a key is unavoidable, I give its user **no permission except `sts:AssumeRole` on one role**. The real permissions live on the role, sessions expire and can be revoked. Full walkthrough: [[Assuming a role step by step]].

## Access Advisor

<span style="color:rgb(255, 192, 0)"><b>Access Advisor</b></span> shows **when a user/role last used each AWS service**, so I can find permissions nobody uses and remove them (least privilege).

```
Service       Last accessed
────────────────────────────
EC2           Sep 20, 2026
S3            Sep 19, 2026
RDS           Sep 10, 2026
DynamoDB      Never          ← remove this permission?
Lambda        Never
CloudWatch    Sep 20, 2026
IAM           Aug 02, 2026
```

### Access Advisor vs CloudTrail
<span style="color:rgb(192, 0, 0)">This distinction comes up in AWS exams.</span>

| | Access Advisor | [[CloudTrail]] |
|---|---|---|
| Answers | "When did this principal last use this **service**?" | "**Who** did **which action** on **which resource**, from **where**, **when**?" |
| Detail | Service level | Every single API call |
| Used for | Trimming unused permissions | Auditing, investigations |

CloudTrail example:
```
IAM Role: AppRole
Action:   s3:GetObject
Resource: arn:aws:s3:::my-bucket/file.txt
Time:     14:32
Source IP: ...
```

## Connects to
- [[STS]]: how roles are assumed and temporary credentials issued, trust policies, external ID, GitHub OIDC, why roles beat users with permissions. Hands-on: [[Assuming a role step by step]], and for CI/CD (Continuous Integration / Continuous Delivery) [[Connecting GitHub Actions to AWS]]
- [[ARN]]: how policies point at resources
- [[AWS Organizations]]: SCPs **cap** what IAM can grant
- [[AWS Identity Center]]: the modern way for people to log in (instead of IAM users)
- [[CloudTrail]]: records everything IAM identities do. Debugging AccessDenied and tracing a role session to a person → [[CloudTrail in production]]
- [[EC2]], [[Lambda]]: get permissions through roles
- [[S3]]: bucket policies are the resource-based policy I'll write most, and cross-account access needs both sides
- Big picture → [[How AWS services connect]]
- How API calls are authenticated (SigV4) → [[HMAC request signing]]; the general authN vs authZ picture → [[Authentication and authorization]]; MFA → [[Multi-factor authentication and passkeys]]

## Flashcards
#flashcards

User vs role? :: A user has long-term credentials. A role has none and is assumed temporarily (by services, other accounts, SSO users)
If one policy allows and another denies the same action? :: Explicit Deny always wins
How should an EC2 instance get S3 access? :: An IAM role (instance profile), never access keys on disk
Access Advisor vs CloudTrail? :: Access Advisor shows the last time a service was used. CloudTrail logs every API call in detail
What should the root user be used for? :: Almost nothing: initial setup and root-only tasks. Protect it with MFA
Trust policy vs permissions policy of a role? :: Trust policy = who may assume the role. Permissions policy = what it can do once assumed
How many access keys can an IAM user have? :: Two, so one can be rotated while the other is still in use
When can you see an access key's secret? :: Only once, at creation. Lost = create a new key
Which create-role trusted entity type do you pick for GitHub Actions? :: Web identity (an OIDC provider), with conditions on the repository/branch
