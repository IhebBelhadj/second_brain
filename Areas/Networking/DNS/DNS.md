---
type: subtopic
created: 2026-10-09
topic: Networking
tags: [subtopic, networking]
aliases: [Domain Name System]
---
# DNS

> What this covers: name resolution, its security and running it in production.

Part of [[Networking]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[DNS basics]]: why it's a delegated tree, the three roles (stub, recursive, authoritative), a lookup step by step, caching and TTL, records, glue, how Linux resolves, reading `dig`
- [[DNS security]]: cache poisoning and Kaminsky, DNSSEC's chain of trust, DoT/DoH, hijacking, subdomain takeover, tunneling, amplification, rebinding
- [[DNS in production]]: internal naming, split-horizon, hybrid forwarding, DNS load balancing and its limits, safe record changes, running servers, a troubleshooting method

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
