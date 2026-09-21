---
type: note
created: 2026-09-20
topic:
tags: []
---
# AWS Organizations

> **AWS Organizations** is a service that lets you **centrally manage multiple AWS accounts** as one organization.
> 
> Instead of having 20 AWS accounts that you manage independently, you can put them under one organization and apply centralized policies, billing, and governance.

> <span style="color:rgb(255, 192, 0)">Very important Note : </span>
> now you might be asking well don't we have IAM to manage users why would we need another layer on top of management while we can group users in groups and assign security policies to these and we're done with access control 
> > Yes and no well in AWS there is a difference between 
> 

Here is the hierarchy and the relationship between organizations and IAM 

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

An Organizational Unit (OU) is a simple container for AWS accounts
Here is an example (Btw you can nest OUs together): 

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

Now here comes the important part , the equivalent of policies in an IAM is SCP (Service Control Policy) when it comes to AWS organizations 

> An **SCP (Service Control Policy)** defines the **maximum permissions available to principals in member accounts**.
> <span style="color:rgb(255, 192, 0)">Important : It does <b>not grant permissions</b>.</span>
> Permission granting is the job of the IAM service which adds policies to users but these policies would be limited in their access by the SCPs defined by that account
> <span style="color:rgb(0, 112, 192)">IAM policy → grants permissions</span>
> <span style="color:rgb(0, 112, 192)">SCP → limits maximum permissions</span>
> 
> Thus you get this diagram : 

```
IAM permissions
        ∩
SCP permissions
        =
Effective permissions
```

**Here is a concrete example:** 
suppose you have this SCP : 
```
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
now when you create an admin role with this policy  :
```
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
even though you should be allowed to terminate an EC2 instance based on what we have defined in the IAM policy but since we denied it in the SCP we won't be able to complete such an action  

here are the services offered by aws organizations : 

```
                  AWS Organizations
                         │
       ┌─────────────────┼──────────────────┐
       │                 │                  │
       ▼                 ▼                  ▼
      SCPs        Consolidated billing   Account management
       │
       ▼
   Governance
```

### When this comes in handy

Organization rules through SCPs (Service Control Policies) come in handy when it comes to <span style="color:rgb(255, 192, 0)">denying permissions for a group of accounts </span>

example : 
Nobody in any of our 50 AWS accounts can use `ap-southeast-1`
#### With only IAM

You'd need to make sure the appropriate IAM policies in **each account** enforce that restriction.

```
Account 1 → IAM policy
Account 2 → IAM policy
Account 3 → IAM policy
...
Account 50 → IAM policy
```

That's difficult to govern consistently.

#### With Organizations + SCP

You can put the accounts under an OU:

```
                   Organization
                        │
                   Workloads OU
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
    Account A       Account B       Account C
        │               │               │
        └───────────────┼───────────────┘
                        │
                       SCP
                        │
              Deny ap-southeast-1
```

### Distinction between a user and an account

an account can have multiple users : 
```
                AWS Account
              ┌───────────────────────┐
              │                       │
              │   IAM                 │
              │   ├── Alice           │
              │   ├── Bob             │
              │   └── AdminRole       │
              │                       │
              │   AWS Resources       │
              │   ├── EC2             │
              │   ├── S3              │
              │   └── RDS             │
              │                       │
              └───────────────────────┘
```

on account on the other hand has much more context than being a simple user since it has: 
- Its own account ID.
- Its own billing boundary.
- Its own IAM configuration.
- Its own AWS resources.
- Its own regional resources.
- Its own security and administrative boundaries.

#### <span style="color:rgb(255, 192, 0)">Can one user access multiple AWS accounts?</span>

in the **traditional IAM approach**
You could create separate IAM users in each account:

```
Production Account
└── IAM User: Alice

Development Account
└── IAM User: Alice

Security Account
└── IAM User: Alice
```

but in **Modern approach**

```
```
using the <span style="color:rgb(255, 192, 0)">IAM Identity Center</span> (more on that here [[AWS Identity Center]])
a user can have one central identity and access multiple AWS accounts

### AWS Control Tower vs Organizations

Provides a more opinionated framework for **setting up and governing a multi-account AWS environment**.

Conceptually:
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


### Quick summary 

|Component| Responsibility### Destinction between a user and an account |Example|
| ----------------------- | ----------------------------------------------------------- | --------------------------------- |
|**OU**| Groups AWS accounts                                         |Production accounts|
|**SCP**| Restricts maximum permissions for accounts                  |Block EC2 termination|
|**IAM**| Manages permissions within an account                       |Allow Alice to read S3|
|**IAM Identity Center**| Centrally assigns user access to accounts                   |Alice gets ReadOnly in Production|
### Creating and managing Organizations

inside the organization you will find all the **organization units** (**OUs**) you have defined : 
![[Pasted image 20260920205439.png]]

Creating a new organization unit is a straight forward process just provide a name with optional tags : 
![[Pasted image 20260920205530.png]]

>To these OUs you can append other OUs or add AWS accounts : 
>Here is the form for creating a new aws account


![[Pasted image 20260920205624.png]]

