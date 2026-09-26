---
type: topic
created: 2026-09-26
tags: [topic]
---
# Networking

> What this covers: the general networking stuff (protocols, routing) that sits underneath the cloud. Not AWS-specific, but AWS makes a lot more sense once I know it.

## Start here
- [[ICMP]]: what `ping` actually uses (and why a security group can block it)
- [[AS and BGP]]: how the internet routes between networks. It shows up in AWS as the ASN on a transit gateway

## Where this shows up in AWS
- [[VPC]]: subnets, CIDR ranges, route tables
- [[Connecting VPCs]]: transit gateways use ASNs / BGP
- [[Route 53]]: DNS
- [[Load balancers]]: Layer 4 vs Layer 7

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE topic = this.file.name AND confidence
SORT confidence ASC
```

## Open questions
- OSI layers properly: I keep saying "L4" and "L7" without being 100% sure of the rest
