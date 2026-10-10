---
type: subtopic
created: 2026-10-09
topic: Networking
tags: [subtopic, networking]
---
# Local area networks

> What this covers: Layer 2: switches, ARP, VLANs, Spanning Tree.

Part of [[Networking]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[Hubs, switches and routers]]: what each device decides on, MAC learning, ARP, collision vs broadcast domains, why the home "router" is five devices
- [[ARP]]: how IP finds MAC, the packet, cache states, gratuitous and proxy ARP, failover and duplicate-IP problems, ARP spoofing and defenses, NDP and clouds
- [[VLAN]]: virtual switches, access vs trunk ports, 802.1Q, native VLAN traps, routing between VLANs
- [[Spanning Tree]]: why redundant switch links loop forever, how STP/RSTP block them, how data centers design loops out

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
