---
type: note
created: 2026-09-20
topic:
tags: []
---
# VPC

> **One sentence: what is this?**
  Its an isolated virtual network

## Different services VPC provides

| Service                                               | Role                                                         |
| ----------------------------------------------------- | ------------------------------------------------------------ |
| Subnets                                               | Creating network subnets                                     |
| Routing tables                                        | Used to define how routing would work inside a network       |
| Internet Gateways                                     | Define an internet connection gateway per VPC                |
| NAT Gateway                                           | Enables outbound IPv4 internet access from private resources |
| Security Group                                        | Controls traffic at the resource level                       |
| <span style="color:rgb(192, 0, 0)">Network ACL</span> | Controls traffic at the subnet level                         |
| Elastic IP                                            | Provides a static public IPv4 address                        |

COLOR MAP : 
- <span style="color:rgb(192, 0, 0)">Not learned yet</span>
- <span style="color:rgb(255, 192, 0)">Just a small encounter</span>
- <span style="color:rgb(146, 208, 80)">Mid knowledge</span>
- <span style="color:rgb(0, 112, 192)">Good Grasp</span>



> **NOTE:**  The subnet you create would be public or private depending on the routing table setup inside the VPC : 
>  - Public subnet means there is a network IP that maps to an internet gateway in the routing table in which this subnet belongs
>  - Private subnet means there is no internet gateway connction in the routing table in which this subnet belongs

> **NOTE**: Some resources, such as Elastic IPs, have broader AWS service associations, but they integrate directly with VPC networking.
> example : Elastic IP is associated with [[EC2]] and [[VPC]]
## Open questions

- [ ] How would a service like a web service in a public subnet connect to a db or other cluster of backend services sitting behind a private subnet which has its own routing table ?

## Services

### NAT Gateway

**NAT Gateway (Network Address Translation Gateway):**  An AWS-managed networking resource deployed in a public subnet that ==enables resources in private subnets to establish outbound IPv4 connections to the internet without requiring public IP addresses.==

It translates the private source IP addresses of outgoing traffic into a public IP address and maintains connection state so that response traffic can return to the originating resources. External users cannot initiate unsolicited connections to resources behind the NAT Gateway.

NAT Gateways are useful when private resources, such as EC2 instances or application servers, need internet access to download packages, install dependencies, retrieve updates, or communicate with external APIs.


## Why it matters


## Links
- 
