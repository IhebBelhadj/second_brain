---
type: note
created: 2026-09-20
topic:
tags: []
---
# Root user vs IAM user

when you first log into AWS you will use the root user to create other IAM users (I**dentity Access Management**) which in turn manage the resources on AWS depending on the permissions. 
It is highly recommended to limit your usage of the root user and only use it for administrative purposes only 

![[Pasted image 20260920193211.png]]

> To control the access of the created users you would need to create policies and assign these policies to these users or user groups if you want to organize access control by groups 

> A policy is nothing but an access grant over a resource (and that access can be granular 
> for example you can only view but you cannot create items on that resource etc ...)

Here is the basic interface for the **IAM Service**

![[Pasted image 20260920193711.png]]

When creating users you'll be prompted to add the user to a group or assign permissions directly to it, please not that in production systems its highly recommended to organize policies and access grants into groups and assign the created users to these groups 
 ![[Pasted image 20260920193901.png]]

> Note: Please note that when creating a user , just like with any resource you create on AWS you get a unique resource identifier which is the <span style="color:rgb(255, 192, 0)">ARN</span> (**Amazon Resource Name**) for more informations about ARN see [[ARN]]

![[Pasted image 20260920194115.png]]

to enable access to this user you would need to add access to the console to this user in the security credentials tab

### Creating policies

![[Pasted image 20260920201531.png]]

This is the interface to create policies where you can use the visual editor to create a policy with certain permissions or insert a json object like this : 

![[Pasted image 20260920193547.png]]

For creating groups here is the group inspection view : 
![[Pasted image 20260920201941.png]]

<span style="color:rgb(255, 192, 0)"><b>Access Advisor</b></span> : **AWS IAM Access Advisor** is a feature in **AWS IAM** that helps you determine **which AWS services an IAM principal has actually accessed**.

> The key idea is:
> **Access Advisor tells you when an IAM user or role last used each AWS service.**

Access Advisor might show:

```
Service       Last accessed
────────────────────────────
EC2           Sep 20, 2026
S3            Sep 19, 2026
RDS           Sep 10, 2026
DynamoDB      Never
Lambda        Never
CloudWatch    Sep 20, 2026
IAM           Aug 02, 2026
```

## Access Advisor vs CloudTrail

<span style="color:rgb(192, 0, 0)">This distinction is important for AWS exams.</span>
> For more informations about CloudTrail refer to [[CloudTrail]]

### Access Advisor

Answers: **"When was this IAM principal's last access to this AWS service?"**
It's useful for identifying **unused service permissions**.

### CloudTrail

Answers much more detailed questions:
**"Who performed what API action, on which resource, from where, and when?"**

For example:

```
IAM Role: AppRole
Action: s3:GetObject
Resource: arn:aws:s3:::my-bucket/file.txt
Time: 14:32
Source IP: ...
```