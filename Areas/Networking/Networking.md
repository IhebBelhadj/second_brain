---
type: topic
created: 2026-09-26
tags: [topic]
---
# Networking

> What this covers: the general networking stuff (protocols, routing) that sits underneath the cloud. Not AWS-specific, but AWS makes a lot more sense once I know it.

## Start here
- [[Network layers]]: OSI vs TCP/IP, what's inside an Ethernet frame / IP / TCP header, and security at each layer. The map everything else hangs on
- [[ICMP]]: what `ping` actually uses (and why a security group can block it)
- [[ACL]]: access control lists, the "ordered list of allow/deny rules" idea behind AWS Network ACLs and WAF web ACLs
- [[AS and BGP]]: how the internet routes between networks. It shows up in AWS as the ASN on a transit gateway

## Interfaces (where the machine meets the network)
- [[Network interfaces]]: physical NICs, virtual ones (loopback, bridge, veth, tun/tap, VLAN, VXLAN, WireGuard…), namespaces, Docker, AWS ENIs

## Local networks (Layer 2)
- [[Hubs, switches and routers]]: what each device decides on, MAC learning, ARP, collision vs broadcast domains, the home "router" that's five devices
- [[VLAN]]: virtual switches, access vs trunk ports, 802.1Q, native VLAN traps, inter-VLAN routing
- [[Spanning Tree]]: why redundant switch links loop forever, how STP/RSTP block them, and how data centers design loops out

## Routing (where packets go)
- [[Routing tables]]: longest prefix match, metrics, admin distance, Linux's multiple tables
- [[Policy-based routing]]: `ip rule`, marks, VRFs and namespaces. Choosing *which* table before choosing the route
- [[NAT and PAT]]: static/dynamic NAT, PAT tables, SNAT vs DNAT, NAT types and hole punching, CGNAT, why NAT isn't a firewall, AWS NAT gateway
- [[Overlapping address spaces]]: when two networks use the same IPs, and the ways out (PBR, NAT, PrivateLink, renumbering)

## Security (protecting traffic)
- [[Encryption basics]]: symmetric vs asymmetric, Diffie-Hellman, forward secrecy, certificates
- [[TLS]]: protects one application's connection (HTTPS, termination at the ALB)
- [[mTLS]]: both sides show certificates. Service-to-service auth, IoT, B2B, ALB/API Gateway mTLS
- [[Certificates and PKI]]: what's in a certificate, chains, trust stores, public vs private CAs, file formats
- [[Workload identity (SPIFFE)]]: identities for services without stored secrets (SPIFFE/SPIRE, IAM Roles Anywhere)
- [[Service mesh]]: proxies + control plane doing mTLS, authorization, retries and traffic splitting for every service
- [[Certificate rotation]]: renewing certificates automatically (ACME, ACM, CA rotation)
- [[ACL]]: ordered allow/deny rule lists

## VPNs (joining networks over the internet)
- [[VPN]]: types, how a client works (tun, routes, DNS), split vs full tunnel, WireGuard, MTU
- [[Types of VPN]]: site-to-site → DMVPN → SD-WAN, remote access → ZTNA, mesh overlays and NAT hole punching, L2 VPNs, MPLS. Each one as the fix for the previous one's problem
- [[IPsec and IKE]]: ESP, IKEv2 exchanges, policy- vs route-based, NAT-T, AWS Site-to-Site VPN
- [[IPsec vs TLS vs WireGuard vs SSH]]: which one to use when
- [[Connecting AWS to a private network]]: workarounds to the managed VPN, and why each one breaks

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
- ~~OSI layers properly: I keep saying "L4" and "L7" without being 100% sure of the rest~~ → answered in [[Network layers]]
