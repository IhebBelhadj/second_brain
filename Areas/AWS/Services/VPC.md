---
type: note
created: 2026-09-20
topic:
tags: []
---
# VPC

> **One sentence: what is this?**
  Its an isolated virtual network

![[Pasted image 20260920090454.png]]
## Different services VPC provides

| Service                                               | Role                                                                        |
| ----------------------------------------------------- | --------------------------------------------------------------------------- |
| VPC                                                   | Defined by a primary IPv4 CIDR (/16–/28); supports secondary CIDRs and IPv6 |
| Subnets                                               | Creating network subnets                                                    |
| Routing tables                                        | Used to define how routing would work inside a network                      |
| Internet Gateways                                     | Define an internet connection gateway per VPC                               |
| NAT Gateway                                           | Enables outbound IPv4 internet access from private resources                |
| Security Group                                        | Controls traffic at the resource level                                      |
| <span style="color:rgb(192, 0, 0)">Network ACL</span> | Controls traffic at the subnet level                                        |
| Elastic IP                                            | Provides a static public IPv4 address                                       |
| MORE                                                  | ==These are only the important ones==                                       |

COLOR MAP : 
- <span style="color:rgb(192, 0, 0)">Not learned yet</span>
- <span style="color:rgb(255, 192, 0)">Just a small encounter</span>
- <span style="color:rgb(146, 208, 80)">Mid knowledge</span>
- <span style="color:rgb(0, 112, 192)">Good Grasp</span>
- Not sure



> **NOTE:**  The subnet you create would be public or private depending on the routing table setup inside the VPC : 
>  - Public subnet means there is a network IP that maps to an internet gateway in the routing table in which this subnet belongs
>  - Private subnet means there is no internet gateway connction in the routing table in which this subnet belongs

> **NOTE**: Some resources, such as Elastic IPs, have broader AWS service associations, but they integrate directly with VPC networking.
> example : Elastic IP is associated with [[EC2]] and [[VPC]]
## Open questions

- [ ] How would a service like a web service in a public subnet connect to a db or other cluster of backend services sitting behind a private subnet which has its own routing table ?
- [ ] What are the naming conventions for service instances in AWS
- [ ] What are the norms of availaibilty zones for disaster recoveries

## Services

### NAT Gateway

**NAT Gateway (Network Address Translation Gateway):**  An AWS-managed networking resource deployed in a public subnet that ==enables resources in private subnets to establish outbound IPv4 connections to the internet without requiring public IP addresses.==

It translates the private source IP addresses of outgoing traffic into a public IP address and maintains connection state so that response traffic can return to the originating resources. External users cannot initiate unsolicited connections to resources behind the NAT Gateway.

NAT Gateways are useful when private resources, such as EC2 instances or application servers, need internet access to download packages, install dependencies, retrieve updates, or communicate with external APIs.

### Internet Gateway

> Creating an internet gateway requires only a name with optional tags
><span style="color:rgb(0, 112, 192)"> IMPORTANT NOTE: </span> The IGW needs to be attached to a VPC


![[Pasted image 20260920090600.png]]

![[Pasted image 20260920090821.png]]

### Subnets

> To create a subnet you need to assign VPC (Since subnets should fall under the IP range of that VPC)
> You can click on add subnet button to add a subnet (batch subnet creation form)

![[Pasted image 20260920091146.png]]


<span style="color:rgb(255, 192, 0); font-weight: bold">Availability Zone</span> : AZs are discrete data centers within AWS regions physically seperated with the goal of failure isolation (a flood , a fire event , etc ... should not take down a service from another availability zone)

> <span style="color:rgb(192, 0, 0)">Important note : </span> A network subnet can only be assigned to a single route table where as a route table can have multiple subnets assigned to it

### Route tables

![[Pasted image 20260920092453.png]]

> Route table creation is very simple just add a name 
> ==Route definitions are set after the creation process ==

![[Pasted image 20260920093146.png]]

<span style="color:rgb(255, 192, 0)">Subnet Association</span> : 

![[Pasted image 20260920093403.png]]


## Links
- 
