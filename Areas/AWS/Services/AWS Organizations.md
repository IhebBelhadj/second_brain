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

> Very important Note : 
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

inside the organization you will find all the **organization units** (**OUs**) you have defined : 
![[Pasted image 20260920205439.png]]

Creating a new organization unit is a straight forward process just provide a name with optional tags : 
![[Pasted image 20260920205530.png]]

>To these OUs you can append other OUs or add AWS accounts : 
>Here is the form for creating a new aws account


![[Pasted image 20260920205624.png]]

