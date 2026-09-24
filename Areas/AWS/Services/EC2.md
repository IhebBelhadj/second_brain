---
type: note
created: 2026-09-20
topic:
tags: []
---
# EC2

> Creating a VM with an image (AMI) where your compute should live 

### Creation process of an EC2

![[Pasted image 20260920093658.png]]

> For logging into this EC2 instance to provision it from your machine you need a key pair 

![[Pasted image 20260920093859.png]]


![[Pasted image 20260920094227.png]]

> In the network tab of the EC2 instance creation process you can assign network settings like assigning a ==security group==
> - In the network tab you can also assign to which VPC as well as which subnet this EC2 belongs to

<span style="color:rgb(255, 192, 0)">Security Groups</span> : A security group is a set of firewall rules that control the traffic for your instance


### EC2 Launch Templates

> You can use this feature of the EC2 service to kick start EC2 instances without relying on manual setup on the UI each time

![[Pasted image 20260924191504.png]]

here is the form UI for creating a launch template : 
![[Pasted image 20260924191614.png]]

![[Pasted image 20260924192121.png]]

<span style="color:rgb(255, 192, 0)">Note : </span>The UI for creating a launch template is basically the same as creating an EC2 instance manually

Now to create a new EC2 instance based on the newly created launch template you can simply opt for the option launch instance from template 
![[Pasted image 20260924192453.png]]


### Target groups

## Open questions 

- [ ] What is the difference between RSA and ED25519 and what is also the difference between OpenSSH and PuTTY ? 
- [ ] If my EC2 instance sits behind a private IP then how come I can SSH into it ?

