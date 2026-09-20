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

Here is an example policy : 
![[Pasted image 20260920193547.png]]

Here is the basic interface for the **IAM Service**

![[Pasted image 20260920193711.png]]

When creating users you'll be prompted to add the user to a group or assign permissions directly to it, please not that in production systems its highly recommended to organize policies and access grants into groups and assign the created users to these groups 
 ![[Pasted image 20260920193901.png]]

> Note: Please note that when creating a user , just like with any resource you create on AWS you get a unique resource identifier which is the <span style="color:rgb(255, 192, 0)">ARN</span> (**Amazon Resource Name**)

![[Pasted image 20260920194115.png]]
## In my own words


## Why it matters


## Links
- 
