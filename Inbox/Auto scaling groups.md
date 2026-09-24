---
type: note
created: 2026-09-24
topic:
tags: []
---
# Auto scaling groups

> One sentence: what is this?

![[Pasted image 20260924204403.png]]

Here is the diagram for the desired architecture 

![[Pasted image 20260924204451.png]]

when creating the launch template there is a warning when assigning subnet for that you need to remove subnet for ec2 auto scaling
![[Pasted image 20260924204543.png]]

don't forget to enable auto assign public IP address to have a public IP for each generated instance 

![[Pasted image 20260924204914.png]]

this is the multi step form for creating an auto scaling group 

We can assign a load balancer to that auto scaling group we are creating which would show us the target group we created since the load balancer is already assigned to that target group (see the diagram above for the whole architecture as reference)
![[Pasted image 20260924205033.png]]

![[Pasted image 20260924205226.png]]
<span style="color:rgb(0, 112, 192)">What is the VPC lattice service ? </span> I don't know yet (==to be studied==)

![[Pasted image 20260924205344.png]]

for health checks make sure to turn on elastic load balancing health checks which will make this auto scale group react to health check returns of instances 

![[Pasted image 20260924205449.png]]

This is the step where we put our desired capacity 

![[Pasted image 20260924205626.png]]