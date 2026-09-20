---
type: note
created: 2026-09-20
topic:
tags: []
---
# How to connect multiple VPCs

### The standard Peering connection option in the VPC service

![[Pasted image 20260920155305.png]]

In the VPC service on AWS there is the option for ==Peering connections== , you'll be prompted with this form : 

![[Pasted image 20260920155420.png]]

its a simple form where you select the local vpc and the other VPC to peer with (nothing fancy here)

> Note: in this case the VPC to peer with should accept the peering connection request

![[Pasted image 20260920155716.png]]

![[Pasted image 20260920155819.png]]

after that you would need to udate the route table lets pick the route table for VPC 1 to do the setup : 
![[Pasted image 20260920155931.png]]

![[Pasted image 20260920160057.png]]

> we need to add a new connection to the route table with the destination being the other VPC's IP range with the connection type being a peering connection and select the adequate peering connection from the dropdown

we will do the same with the VPC-2 route table where we will put a destination with the first VPC's IP range with the adequate peering connection as well 

![[Pasted image 20260920160254.png]]

### Transitive routing
Here is another more robust way to connect VPCs toghether which is to use a ==transitive gateway==
