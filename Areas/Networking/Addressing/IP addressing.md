---
type: subtopic
created: 2026-10-09
topic: Networking
tags: [subtopic, networking]
---
# IP addressing

> What this covers: IP addresses, subnetting and designing an address plan.

Part of [[Networking]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[IP addressing and subnetting]]: what an address is in binary, masks and prefixes, the mental method, special ranges, VLSM design, summarization, planning a real address scheme, with practice exercises
- [[IP address planning]]: designing the plan itself. One aligned block per group so routes and firewall rules aggregate, a hierarchy of bits (environment vs region first), sizing for growth, reserved ranges, ranges to avoid, IPAM as the source of truth

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
