---
type: concept
created: 2026-09-20
topic: AWS
confidence: 2
tags: [aws, security]
---
# IAM

> [!abstract] In one sentence
> IAM (**Identity and Access Management**) decides **who** (a user, or a service like EC2/Lambda) can do **what** on **which** resources inside one AWS account.

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
| **Policy** | A JSON document: which **actions** are **allowed/denied** on which **resources** |

> A policy is just an access grant on a resource, and it can be very granular: e.g. "can read items but not create them".

The IAM console:

![[Pasted image 20260920193711.png]]

### Users and groups

When creating a user, I can add it to a group or attach permissions directly. In real life: **put permissions on groups** and put users in groups. It's much easier to manage than 50 users with 50 custom policy sets.
![[Pasted image 20260920193901.png]]

> [!note] Every resource I create gets a unique identifier, its <span style="color:rgb(255, 192, 0)">ARN</span> (**Amazon Resource Name**). More in [[ARN]].

![[Pasted image 20260920194115.png]]

To let the user log into the console, enable **console access** in the *Security credentials* tab.

The group view:
![[Pasted image 20260920201941.png]]

### Creating policies

![[Pasted image 20260920201531.png]]

Either the **visual editor** or raw **JSON**:

![[Pasted image 20260920193547.png]]

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

This is how the services in my other notes get their rights, **without storing keys anywhere**:

| Who | Role | Example |
|---|---|---|
| [[EC2]] instance | Instance profile | The app on the instance reads from S3 |
| [[Lambda]] function | Execution role | The function writes logs, reads a DynamoDB table |
| [[Bastion host]] replacement | Instance role with SSM permissions | Session Manager access with no SSH |
| SSO user | Permission set → role | [[AWS Identity Center]] users assume a role in each account |

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
- [[ARN]]: how policies point at resources
- [[AWS Organizations]]: SCPs **cap** what IAM can grant
- [[AWS Identity Center]]: the modern way for people to log in (instead of IAM users)
- [[CloudTrail]]: records everything IAM identities do
- [[EC2]], [[Lambda]]: get permissions through roles
- Big picture → [[How AWS services connect]]

## Flashcards
#flashcards

User vs role? :: A user has long-term credentials. A role has none and is assumed temporarily (by services, other accounts, SSO users)
If one policy allows and another denies the same action? :: Explicit Deny always wins
How should an EC2 instance get S3 access? :: An IAM role (instance profile), never access keys on disk
Access Advisor vs CloudTrail? :: Access Advisor shows the last time a service was used. CloudTrail logs every API call in detail
What should the root user be used for? :: Almost nothing: initial setup and root-only tasks. Protect it with MFA
