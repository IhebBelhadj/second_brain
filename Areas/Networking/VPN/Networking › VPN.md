---
type: subtopic
created: 2026-10-09
topic: Networking
tags: [subtopic, networking]
---
# Networking › VPN

> What this covers: joining networks: VPN types, IPsec, WireGuard and friends, nested VPNs.

Part of [[Networking]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[VPN]]: the three ingredients, how a client works (tun, routes, DNS), site-to-site vs remote access, split vs full tunnel, WireGuard, MTU
- [[Types of VPN]]: site-to-site → DMVPN → SD-WAN, remote access → ZTNA, mesh overlays and NAT hole punching, L2 VPNs, MPLS. Each one as the fix for the previous one's problem
- [[IPsec and IKE]]: ESP, IKEv2 exchanges, policy- vs route-based, NAT-T, MTU, troubleshooting
- [[IPsec vs TLS vs WireGuard vs SSH]]: which one to use when
- [[Nested VPNs]]: chained VPNs (branch → HQ → cloud, a routing problem: transitivity, selectors, return paths, hairpinning) vs stacked VPNs (tunnel in a tunnel, an MTU problem), and the fixes

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
