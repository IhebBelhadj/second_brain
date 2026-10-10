---
type: subtopic
created: 2026-10-09
topic: Networking
tags: [subtopic, networking]
---
# Network protocols

> What this covers: the layer model and the protocols on top of it: ICMP, HTTP, HTTP/2 and HTTP/3, WebSocket, OSPF, BGP.

Part of [[Networking]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[Network layers]]: OSI vs TCP/IP, what's inside an Ethernet frame / IP / TCP / UDP header, how a request crosses the network hop by hop, and security at each layer. **The map everything else hangs on**
- [[ICMP]]: the control and error messages behind `ping` and `traceroute` (and why blocking all of it breaks things)
- [[HTTP]]: the request/response protocol on top of TCP. Message anatomy, methods (safe/idempotent), status codes, HTTP/1.0 vs 1.1 persistent connections, Content-Length vs chunked, head-of-line blocking and 6 connections per host, the Host header, polling/long polling/SSE/WebSocket, keep-alive 502s
- [[HTTP2]]: same meaning, new framing. Binary frames and streams multiplexed on one connection, ALPN, HPACK, RST_STREAM/GOAWAY, TCP head-of-line blocking, HTTP/3 over QUIC, the per-connection load balancing trap
- [[WebSocket]]: an HTTP upgrade into a two-way message channel. The handshake (`101`, Sec-WebSocket-Accept), frames and masking, how it crosses NATs, proxies and load balancers (nginx headers, idle timeouts), scaling with a pub/sub backplane, close codes, reconnects, security (Origin, auth), API Gateway WebSocket APIs
- [[OSPF]]: how routers inside one organization find each other. Static routes vs distance-vector rumours (count to infinity) vs link-state (same map everywhere), SPF worked by hand on Acme's four routers, Hellos and what must match, the neighbour states (ExStart, Full), DR/BDR on shared segments, cost and the reference bandwidth trap, ECMP, areas and the backbone, ABR/ASBR, LSA types, stub/NSSA, E1 vs E2, BFD and fast convergence, authentication and passive interfaces, OSPFv3, an FRRouting lab with show commands, vs RIP/IS-IS/BGP, and the classic failures (MTU stuck in ExStart, Init, duplicate router ID, partitioned area 0, redistribution loops)
- [[AS and BGP]]: how independent networks route between each other, the protocol the internet runs on
- ~~OSI layers properly: I keep saying "L4" and "L7" without being 100% sure of the rest~~ → answered in [[Network layers]]

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
