---
type: subtopic
created: 2026-10-09
topic: Networking
tags: [subtopic, networking]
---
# Networking › Traffic

> What this covers: delivering traffic to services: proxies, reverse proxies, load balancing, service discovery, service mesh.

Part of [[Networking]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[Service mesh]]: proxies + a control plane doing mTLS, authorization, retries and traffic splitting for every service
- [[Proxies]]: forward proxies, proxy vs NAT vs VPN, CONNECT, `HTTP_PROXY`/`NO_PROXY`, PAC/WPAD, transparent proxies, SOCKS, TLS inspection and what it breaks
- [[Reverse proxy]]: one entry point for many apps, TLS termination, the "real client IP" problem (X-Forwarded-For, PROXY protocol), 502/504 debugging, the family (LB, API gateway, CDN, ingress, sidecar)
- [[Load balancing]]: L4 vs L7, algorithms, health checks and their traps, sticky sessions, draining and retries, the gRPC trap, making the LB itself HA (VRRP, ECMP, anycast, DSR), global load balancing
- [[Service discovery]]: from config files to DNS to registries, client-side vs server-side, registration, how Kubernetes Services work, failure modes

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
