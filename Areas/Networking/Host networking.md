---
type: subtopic
created: 2026-10-09
topic: Networking
tags: [subtopic, networking]
---
# Host networking

> What this covers: where one machine meets the network: interfaces and namespaces, sockets. How processes on one machine talk to each other (pipes, signals, Unix sockets, shared memory) is in [[Processes]].

Part of [[Networking]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[Network interfaces]]: physical NICs and virtual ones (loopback, bridge, veth, tun/tap, VLAN, VXLAN, WireGuard), network namespaces, how containers and VMs get connected
- [[Sockets]]: the kernel object behind every connection. The system calls (socket, bind, listen, accept, connect), the 5-tuple, `ss`, refused vs timed out, 127.0.0.1 vs 0.0.0.0, event loops and fd limits, byte streams vs messages, TIME_WAIT and CLOSE_WAIT, ephemeral port exhaustion, accept queue overflow

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
