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

> In short : a **Target Group** is a collection of destinations—such as EC2 instances, containers, or IP addresses—that receive traffic from a **load balancer**

> This is an abstraction created so that you separate concern between handling routing itself and handling other concerns like instances health and maintaining the group instances in general (you also have a generic abstraction that you can use anywhere when it comes to load balancing and potentially other concerns (need to verify that))


![[Pasted image 20260924194236.png]]

as you can see you can add a taget group of : 

| Target type  | Example                                                             |
| ------------ | ------------------------------------------------------------------- |
| **Instance** | EC2 instances                                                       |
| **IP**       | Private IP addresses, commonly containers/services                  |
| **Lambda**   | Lambda functions                                                    |
| **ALB**      | An Application Load Balancer as a target in supported architectures |

After defining such a group you can forward traffic to it through  a load balancer : example 

```

                     ┌── EC2 Instance A : port 8080
Internet             │
   │                 │
   ▼                 ▼
Application  →  Target Group
Load Balancer        ▲
   (ALB)             │
                     └── EC2 Instance B : port 8080
                     

Listener:
HTTPS :443
     │
     ▼
Forward to → my-app-tg
```

Important: Health checks are important

The target group also defines how AWS determines whether your application instances are healthy.

AWS periodically requests:
```
http://EC2-A:8080/health
http://EC2-B:8080/health
http://EC2-C:8080/health
```

if an instance becomes unhealthy the load balancer stops sending normal traffic to EC2-B until it becomes healthy again.

![[Pasted image 20260924195037.png]]

after adding insteances they will be included as pending

**Here is the interface for a target group**
![[Pasted image 20260924195127.png]]

![[Pasted image 20260924195206.png]]

note for the instances we included the health check is unused because we did not yet create a load balancer that targets this target group 




## Open questions 


- [ ] What is the difference between RSA and ED25519 and what is also the difference between OpenSSH and PuTTY ? 
- [ ] If my EC2 instance sits behind a private IP then how come I can SSH into it ?

