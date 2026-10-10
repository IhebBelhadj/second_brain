---
type: subtopic
created: 2026-10-09
topic: Networking
tags: [subtopic, networking]
---
# Routing

> What this covers: Layer 3: routing tables, policy routing, NAT, overlapping ranges, high availability.

Part of [[Networking]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[Routing tables]]: longest prefix match, metrics, administrative distance, Linux's multiple tables
- [[Policy-based routing]]: `ip rule`, marks, VRFs and namespaces. Choosing *which* table before choosing the route
- [[NAT and PAT]]: static/dynamic NAT, PAT tables, SNAT vs DNAT, NAT behaviors and hole punching, CGNAT, UPnP/NAT-PMP/PCP, why NAT isn't a firewall
- [[Outbound-initiated connections]]: responses vs new connections through NAT, why an HTTP response doesn't end the TCP connection, why a NAT mapping isn't an open door, agents that dial out and keep the line open (SSM, CI runners, tunnels), keepalives, the egress-control lesson
- [[Overlapping address spaces]]: two networks using the same IPs, and the ways out (separate routing domains, NAT, exposing services, renumbering)
- [[High availability networking]]: where "replicate it" stops (the gateway for the gateways). One address, one machine; multiple A records and their limits; one address served by several machines: floating IP (VRRP) on a LAN, ECMP in a site, anycast across networks; DNS vs BGP jobs; hierarchy vs distributed graph; redundancy at every level (DNS root included); black holes, split brain, ECMP rehash, shared fate, slow failover

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
