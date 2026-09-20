---
type: note
created: 2026-09-20
topic:
tags: []
---
# VPC

> One sentence: what is this?

## Different services VPC provides

| Service           | Role                                                   |
| ----------------- | ------------------------------------------------------ |
| Subnets           | Creating network subnets                               |
| Routing tables    | Used to define how routing would work inside a network |
| Internet Gateways | Define an internet connection gateway per VPC          |
| NAT Gateway       |                                                        |
| Security Group    |                                                        |

> **NOTE:**  The subnet you create would be public or private depending on the routing table setup inside the VPC : 
>  - Public subnet means there is a network IP that maps to an internet gateway in the routing table in which this subnet belongs
>  - Private subnet means there is no internet gateway connction in the routing table in which this subnet belongs
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
