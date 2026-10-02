---
type: concept
created: 2026-09-27
topic: Networking
confidence: 1
tags: [networking, load-balancing, high-availability]
aliases: [Load balancer, L4 load balancing, L7 load balancing, Health checks, Sticky sessions, Direct server return, GSLB]
---
# Load balancing

> [!abstract] In one sentence
> A load balancer spreads incoming work across several servers and **stops sending to the ones that are down**, so the service survives failures and can grow by adding servers. The real design choices are **which layer it works at** (L4 connections vs L7 requests), **how it picks a server**, **how it knows a server is healthy**, and **how the load balancer itself avoids being the single point of failure**.

## The misconception I had

**Wrong mental model:** "a load balancer splits traffic evenly, so three servers each get a third of the load."

**What's actually true:**
- It splits **connections** or **requests**, not load. One connection can carry one request or a million (HTTP/2, gRPC, WebSockets), and one request can take 5 ms or 5 minutes
- With long-lived connections, a new server added to the pool gets **nothing** until clients reconnect
- "Evenly" is often wrong anyway: servers differ in size, some requests are heavier, and a server that just started may be slow (cold caches)
- The load balancer's most important job is often not spreading load but **removing failed servers** quickly

## Building it up

### Stage 1: DNS round robin
Several A records for one name (see [[DNS in production#DNS for load balancing and failover]]). Free, but DNS doesn't know which servers are alive, caches pin clients to one answer, and clients handle failures badly. Good enough for coarse, global spreading, not for failover in seconds.

### Stage 2: a box in front
One **virtual IP** (VIP) that clients connect to, and a **pool** of backends behind it. The load balancer picks a backend for each new connection or request, and **health checks** remove dead ones. Now failover takes seconds and servers can be added or removed without clients noticing.

### Stage 3: choosing the layer

| | **Layer 4** (transport) | **Layer 7** (application) |
|---|---|---|
| Sees | IPs, ports, TCP/UDP | The full HTTP request: host, path, headers, cookies |
| Balances | **Connections** (every packet of a connection goes to the same backend) | **Requests** (each request on a connection can go to a different backend) |
| Connection to backend | Forwards packets, or proxies the TCP stream | Always **two connections** ([[Reverse proxy]]) |
| TLS | Passes it through (the backend decrypts), or terminates it | Terminates it (must, to read HTTP) |
| Can do | Any protocol (databases, MQTT, gaming, DNS, SMTP), huge throughput, low latency | Path/host routing, header rewriting, retries, redirects, WAF, per-request stats, gRPC balancing |
| Examples | LVS/IPVS, HAProxy in TCP mode, hardware LBs, cloud network LBs | HAProxy/nginx/Envoy in HTTP mode, cloud application LBs |

## Choosing a backend: algorithms

| Algorithm | How | Good for | Weakness |
|---|---|---|---|
| **Round robin** | Next server in turn | Equal servers, similar requests | Ignores current load |
| **Weighted round robin** | Bigger servers get more turns | Mixed server sizes, canaries (5% to v2) | Still ignores current load |
| **Least connections** | Server with the fewest open connections | Long connections of varying length | Connections ≠ work |
| **Least outstanding requests** | Fewest requests in flight (L7) | Requests of very different durations | Needs L7 |
| **Least response time** | Fastest recent responses | Heterogeneous backends | Can pile onto a server that's fast because it's failing quickly |
| **Random / power of two choices** | Pick 2 at random, send to the less loaded | Many LBs with no shared state | Slightly less even than perfect |
| **Hash (source IP, header, URL)** | Same key → same server | Caches (same URL → same cache server), stickiness without cookies | Uneven if keys are skewed, reshuffles when servers change |
| **Consistent hashing** (ring, Maglev) | Hash keys onto a ring, adding a server moves only ~1/N of keys | Caches, sharded data, big L4 LB fleets | More complex |

## Health checks: the part that actually keeps the service up

The load balancer probes each backend (TCP connect, or HTTP `GET /health` expecting `200`) every few seconds. After N failures it's marked **unhealthy** and gets no new traffic. After M successes, it's back.

**Advanced problems:**
- **Shallow vs deep checks**: a TCP check passes while the app returns 500s. So check an HTTP endpoint. But if `/health` also checks the **database**, then when the database blips, **every** backend fails its check at once, the pool is empty, and the outage is total instead of partial. Rule: health = "can this instance serve?", not "is everything it depends on up?"
- **Fail open**: many load balancers send traffic to **all** backends when **all** are unhealthy, betting that the health check is wrong rather than every server. Good to know when reading an incident
- **Passive health checks** (outlier detection): watch real traffic, and eject a backend that returns too many errors, without waiting for the next probe
- **Flapping**: a server that dies under load, recovers when removed, dies again when added. Needs slow start and investigation, not a shorter interval

## Keeping state: sticky sessions

**The problem:** the app stores the user's session **in memory** on one server. Request 2 lands on another server → "please log in again".

**Fixes, from quick hack to proper:**
1. **Sticky sessions** (session affinity): the LB sets a cookie (or hashes the source IP) so a user keeps hitting the same backend. Works, but load becomes uneven, and when that server dies, its users lose their sessions anyway
2. **Shared session store**: sessions in Redis or a database, any server can handle any request
3. **Stateless**: the session is a signed token (JWT) the client sends each time

Stickiness is a workaround. Being able to send any request to any server is what makes scaling, deployments and failover simple.

## Changing the pool without breaking users

| Feature | Problem it solves |
|---|---|
| **Connection draining** (deregistration delay) | Removing a server during a deploy would cut in-flight requests. Draining: no new requests, existing ones get N seconds to finish |
| **Slow start** | A fresh server (cold caches, JIT not warmed) gets full traffic immediately and falls over. Slow start ramps its share up over a few minutes |
| **Retries with budgets** | Retrying a failed request on another server hides failures, but when everything is slow, retries **multiply** the load (retry storm). Limit retries to a budget (e.g. 10% extra), only retry safe (idempotent) requests |

### The HTTP/2 and gRPC trap
gRPC keeps **one long HTTP/2 connection** and sends every request over it. An L4 load balancer balances **connections**, so each client sticks to one backend forever, and new backends stay idle. Fix: an **L7** balancer that balances each request (streams) inside the connection, or client-side balancing (see [[Service discovery]]), or forcing connections to recycle periodically.

## Making the load balancer itself highly available

A single load balancer is a new single point of failure. How it's solved, in growing scale:

| Setup | How | Used by |
|---|---|---|
| **Active / passive pair** | Two LBs share a **floating IP** with VRRP (keepalived). If the active one dies, the passive one claims the IP (gratuitous ARP, see [[Hubs, switches and routers]]) | Classic on-prem HAProxy/nginx pairs |
| **Active / active with ECMP** | Several LBs announce the **same IP** to the router with BGP. The router spreads flows across them (ECMP, hashing each flow so its packets always hit the same LB) | Large on-prem setups, cloud providers internally |
| **Anycast** | The same IP announced from **several sites** worldwide with [[AS and BGP\|BGP]]. Users reach the nearest site | CDNs, public DNS resolvers, global accelerators |
| **Tiered** | An L4 tier (fast, simple, ECMP) in front of an L7 tier (smart, heavier) | Most big internet services |

### Direct server return (DSR)
For huge download traffic, the LB forwards the request to a backend by rewriting **only the destination MAC** (the backend has the VIP on its loopback), and the backend **replies directly** to the client, bypassing the LB. The LB only handles the small incoming half. Fast, but L4 only, and the backends need special network config.

## Global load balancing (GSLB)
Several regions or data centers: send each user to a healthy, nearby site.
- **DNS-based**: answer with the IP of the best site (health-checked, latency or geo based). Simple, limited by TTLs and resolver location ([[DNS in production]])
- **Anycast**: one IP everywhere, BGP routes each user to the nearest site. Failover at routing speed, no DNS caching problem
- Usually combined: global steering (DNS or anycast) → a regional load balancer → backends

## Software I'll meet

| Software | Notes |
|---|---|
| **HAProxy** | L4 and L7, extremely efficient, rich health checks and stats. The classic |
| **nginx** | Web server + reverse proxy + L7 LB (L4 with the `stream` module) |
| **Envoy** | Built for dynamic environments: configured by API, rich L7, outlier detection, the base of most service meshes and many gateways |
| **LVS / IPVS** | L4 in the Linux kernel. Also what kube-proxy can use |
| **Traefik, Caddy** | Auto-configured from Docker/Kubernetes, automatic certificates |
| **Cloud LBs** | Managed L4/L7, HA built in: see [[Proxies, load balancing and discovery in AWS]] |

```
# HAProxy: L7 with health checks and least connections
frontend web
    bind :443 ssl crt /etc/haproxy/site.pem
    default_backend app
backend app
    balance leastconn
    option httpchk GET /health
    http-check expect status 200
    server app1 10.0.1.11:8080 check inter 5s fall 3 rise 2
    server app2 10.0.1.12:8080 check inter 5s fall 3 rise 2
```

## Easy to get wrong
- Expecting even load from even connection counts (long-lived connections, gRPC)
- Deep health checks that take the whole pool down when a shared dependency blips
- Sticky sessions as the architecture instead of a shared or stateless session
- Retries without limits turning a slowdown into an outage
- No draining: every deploy cuts requests in flight
- A load balancer without redundancy: the new single point of failure
- Forgetting that backends see the LB's IP, not the client's (see [[Reverse proxy]])

## Related
- Built on:: [[Reverse proxy]], [[Network layers]], [[NAT and PAT]] (L4 LBs rewrite addresses)
- Finding backends:: [[Service discovery]]
- Hashing behind it:: [[Hash table]] (why `hash % servers` moves keys)
- Global:: [[DNS in production]], [[AS and BGP]] (anycast, ECMP)
- Service-to-service:: [[Service mesh]]
- Applied:: [[Proxies, load balancing and discovery in AWS]], [[Load balancers]]

## Flashcards
#flashcards

What does a load balancer actually split? :: Connections (L4) or requests (L7), not load
L4 vs L7 load balancing? :: L4 balances connections by IP/port, any protocol. L7 reads HTTP and balances each request, can route by host/path
Round robin vs least connections vs least outstanding requests? :: In turn. Fewest open connections. Fewest requests in flight
Why use consistent hashing? :: Same key → same server, and adding/removing a server only moves ~1/N of the keys
Danger of deep health checks? :: A shared dependency blip fails every backend at once → empty pool, total outage
What is fail open? :: When all backends are unhealthy, the LB sends to all of them anyway
What are passive health checks / outlier detection? :: Ejecting backends based on errors seen in real traffic
Why are sticky sessions a workaround? :: Uneven load, and sessions die with the server. Better: shared store or stateless tokens
What is connection draining? :: A removed backend gets no new requests but existing ones get time to finish
What is slow start? :: A new backend's share ramps up gradually so cold servers aren't overwhelmed
What is a retry storm and the fix? :: Retries multiply load during slowdowns. Retry budgets, only idempotent requests
Why does gRPC break L4 load balancing? :: One long HTTP/2 connection per client carries all requests, so each client sticks to one backend
How does an active/passive LB pair share an IP? :: VRRP (keepalived) floating IP, taken over with gratuitous ARP
How do several active LBs share one IP? :: They announce it with BGP and the router spreads flows with ECMP
What is direct server return? :: The LB rewrites only the MAC, the backend replies directly to the client
Two ways to do global load balancing? :: DNS-based (health/latency/geo answers) and anycast (one IP announced from many sites)
