# Area guide: Networking

**Index:** `Networking.md` is the learning path (9 numbered sections, each assumes the ones above) with a one-line summary of every note and a "Not written yet" roadmap. Read it for *what* a note covers; use this file for *where* it is.

**Scope:** vendor-neutral networking for a systems engineer. Cloud specifics live in `Areas/AWS/` and are linked from here, never mixed in (except a short "In the cloud" / "In AWS" section at the end of a note).

## Folder map

```
Networking/
├── Networking.md                  topic index (the learning path)
├── ACL.md                         allow/deny rule lists, stateless vs stateful
├── Ingress and egress.md          in vs out relative to a boundary, packet vs connection direction, north-south/east-west, egress control and fees
├── Network interfaces.md          NICs, virtual interfaces (bridge, veth, tun/tap, VLAN, VXLAN), namespaces, Docker, ENIs
├── Inter-process communication.md  fds, files, pipes, FIFOs, signals, Unix sockets, shared memory
├── Sockets.md                     socket API, 5-tuple, ss, bind addresses, event loops, framing, TIME_WAIT/CLOSE_WAIT, port exhaustion
├── Service mesh.md                sidecar proxies + control plane, mTLS between services
├── Protocols/                     foundations and protocols
│   ├── Network layers.md          OSI vs TCP/IP, Ethernet frame + IP/TCP/UDP headers, hop-by-hop walk, security per layer
│   ├── ICMP.md                    ping, traceroute, error messages
│   ├── HTTP.md                    messages, methods, status, 1.0 vs 1.1 persistent connections, chunked, HOL, Host, long polling/SSE/WebSocket
│   ├── HTTP2.md                   frames, streams, multiplexing, ALPN, HPACK, TCP HOL, HTTP/3 and QUIC, LB trap
│   ├── WebSocket.md               upgrade handshake, frames/masking, crossing NAT/proxies/LBs, scaling, close codes, security, API Gateway
│   └── AS and BGP.md              inter-network routing, ASNs
├── Addressing/
│   ├── IP addressing and subnetting.md   binary, masks, CIDR, special ranges, VLSM, summarization, practice
│   └── IP address planning.md     hierarchical plans, aggregation, bit budgets, growth, reserved/avoided ranges, IPAM
├── DNS/
│   ├── DNS.md                     resolution, roles, caching/TTL, records, glue, Linux resolver, dig
│   ├── DNS security.md            poisoning, DNSSEC, DoT/DoH, takeovers, tunneling, amplification, rebinding
│   └── DNS in production.md       internal naming, split-horizon, hybrid forwarding, DNS LB, migrations, troubleshooting
├── LAN/                           Layer 2
│   ├── Hubs, switches and routers.md   what each device decides on, MAC learning, domains
│   ├── ARP.md                     IP → MAC, cache states, gratuitous/proxy ARP, failures, spoofing
│   ├── VLAN.md                    802.1Q, access/trunk, native VLAN, inter-VLAN routing
│   └── Spanning Tree.md           L2 loops, STP/RSTP, modern loop-free designs
├── Routing/                       Layer 3
│   ├── Routing tables.md          longest prefix match, metrics, Linux tables
│   ├── Policy-based routing.md    ip rule, marks, VRFs, namespaces
│   ├── NAT and PAT.md             NAT types, PAT tables, SNAT/DNAT, hole punching, CGNAT, NAT ≠ firewall, AWS gateways
│   ├── Outbound-initiated connections.md   responses vs new connections through NAT, agents that dial out (SSM), keepalives
│   ├── Overlapping address spaces.md   same IPs on both sides and the ways out
│   └── High availability networking.md   no gateway for the gateways: multi-A, VRRP floating IP, ECMP, anycast, DNS vs BGP, graph vs hierarchy
├── Security/
│   ├── Encryption basics.md       symmetric/asymmetric, DH, forward secrecy
│   ├── Certificates and PKI.md    certificates, chains, trust stores, CAs
│   ├── TLS.md                     handshake, termination
│   ├── mTLS.md                    client certificates, why a private CA
│   └── Workload identity (SPIFFE).md   service identities without secrets
├── Traffic/                       delivering traffic to services
│   ├── Proxies.md                 forward proxies, CONNECT, HTTP_PROXY, transparent, SOCKS, TLS inspection
│   ├── Reverse proxy.md           TLS termination, X-Forwarded-For, PROXY protocol, 502/504, the family
│   ├── Load balancing.md          L4/L7, algorithms, health checks, stickiness, LB HA, GSLB
│   └── Service discovery.md       DNS vs registries, client/server-side, Kubernetes Services
├── Resilience/                    surviving slow and failing dependencies
│   ├── Resilience patterns.md     hub: timeouts, retries/backoff/jitter, circuit breakers, bulkheads, fallbacks, shedding, hedging, order, app → mesh history
│   ├── Hystrix.md                 tutorial: HystrixCommand, isolation, properties, Spring Cloud, dashboard, migration
│   ├── Resilience4j.md            tutorial: modules, decorators, Spring Boot config/annotations, aspect order, metrics
│   ├── Polly.md                   tutorial (.NET): v7 policies, v8 pipelines, standard resilience handler
│   ├── Resilience libraries in other languages.md   Go, Python, Node.js, gRPC, Failsafe, Sentinel, concurrency-limits, Finagle
│   └── Resilience in a service mesh.md   Istio/Envoy/Linkerd timeouts, retries, budgets, outlier detection, what stays in the app
└── VPN/
    ├── VPN.md                     ingredients, client internals, site-to-site vs remote access, split tunnel, DNS, MTU
    ├── Types of VPN.md            site-to-site → DMVPN → SD-WAN, ZTNA, mesh overlays, L2 VPNs, MPLS
    ├── IPsec and IKE.md           ESP, IKEv2, policy vs route-based, NAT-T, AWS Site-to-Site
    ├── IPsec vs TLS vs WireGuard vs SSH.md   which one when
    └── Nested VPNs.md             chained vs stacked VPNs, transitivity, selectors, hairpin, MTU, in the cloud
```

`Certificate rotation.md` is listed in this area's index (section 6) but the file lives in `Areas/AWS/Security/` with `topic: AWS`.

## Sub-topics

Every note in this area has `subtopic: <index name>` in its frontmatter, and is linked from that sub-topic index (`type: subtopic`, tag `subtopic`). The area index `Networking.md` links every sub-topic index in its "Sub-topics" section.

| Sub-topic index | Lives in | Covers |
|---|---|---|
| `Networking › Protocols.md` | `Protocols/` | the layer model and the protocols on top of it: ICMP, HTTP, HTTP/2 and HTTP/3, WebSocket, BGP |
| `Networking › Host networking.md` | `(area root)` | where one machine meets the network: interfaces and namespaces, inter-process communication, sockets |
| `Networking › Addressing.md` | `Addressing/` | IP addresses, subnetting and designing an address plan |
| `Networking › DNS.md` | `DNS/` | name resolution, its security and running it in production |
| `Networking › LAN.md` | `LAN/` | Layer 2: switches, ARP, VLANs, Spanning Tree |
| `Networking › Routing.md` | `Routing/` | Layer 3: routing tables, policy routing, NAT, overlapping ranges, high availability |
| `Networking › Security.md` | `Security/` | filtering (ACLs, ingress and egress) and securing traffic: encryption, PKI, TLS, mTLS, workload identity |
| `Networking › Traffic.md` | `Traffic/` | delivering traffic to services: proxies, reverse proxies, load balancing, service discovery, service mesh |
| `Networking › Resilience.md` | `Resilience/` | surviving slow and failing dependencies: the patterns, the libraries (Hystrix, Resilience4j, Polly, others) and the service mesh |
| `Networking › VPN.md` | `VPN/` | joining networks: VPN types, IPsec, WireGuard and friends, nested VPNs |

A new note gets the `subtopic` of the folder it goes in (notes at the area root: see the table), and a line in that sub-topic index as well as in `Networking.md`.

## Where a new note goes

| It's about… | Folder |
|---|---|
| A protocol or the layer model (TCP/UDP, HTTP, ICMP, BGP, OSPF) | `Protocols/` |
| Addresses (IPv6, DHCP, subnetting) | `Addressing/` |
| DNS | `DNS/` |
| Layer 2 (Ethernet, Wi-Fi, link aggregation, 802.1X) | `LAN/` |
| Layer 3 forwarding and translation (routing protocols, NAT, VRRP) | `Routing/` |
| Crypto, certificates, identity, firewalls | `Security/` |
| Proxies, load balancing, discovery, CDNs | `Traffic/` |
| Timeouts, retries, circuit breakers, resilience libraries | `Resilience/` |
| VPNs and tunnels | `VPN/` |
| Doesn't fit (troubleshooting, monitoring, automation) | Area root, or a new folder if 2+ notes will share it |

The planned notes (roadmap) are the italic `*[[…]]*` links in `Networking.md`: when writing one, use that exact name so existing links resolve.
