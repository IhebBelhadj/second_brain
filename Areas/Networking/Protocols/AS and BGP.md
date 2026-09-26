---
type: concept
created: 2026-09-20
topic: Networking
confidence: 2
tags: [networking, protocol]
---
# AS and BGP

> [!abstract] In one sentence
> The internet is a mesh of independently run networks called **Autonomous Systems (AS)**, each with its own **AS Number (ASN)**, and **BGP (Border Gateway Protocol)** is the protocol they use to tell each other which IP ranges they can reach.

## In my own words

Each network (an ISP, Google, AWS, a big company) manages its own internal routing. Nobody runs "the internet" centrally, so a **decentralised** protocol is needed between them: that's BGP. Each AS announces "I can reach these IP ranges", and its neighbours decide whether to use and pass on that route.

## BGP vs OSPF

Why BGP, if OSPF already finds shortest paths?

Because between organizations, **shortest isn't the only thing that matters**. Each AS has its own **policies**: business relationships, cost, "don't send my traffic through that competitor", preferred links. OSPF has no way to express that. It just computes the shortest path. BGP is built around policies.

But **inside** an AS, shortest path is exactly what you want, so ASes still use OSPF (or similar) internally:

```
                    INTERNET
                       │
          ┌────────────┴────────────┐
          │          BGP            │
          ▼                         ▼
       AS 100                     AS 200
    ┌─────────┐                 ┌─────────┐
    │  OSPF   │                 │  OSPF   │
    └─────────┘                 └─────────┘
      internal                    internal
       routing                     routing
```

| | BGP | OSPF |
|---|---|---|
| Used | **Between** autonomous systems | **Inside** one AS |
| Decides by | Policies, attributes | Shortest path (cost) |
| Type | Path-vector | Link-state |

## Where it shows up in AWS
- **Transit gateway** creation asks for an **ASN** (see [[Connecting VPCs]])
- **Site-to-Site VPN** and **Direct Connect** use BGP to exchange routes between my data center and AWS

## Connects to
- [[Connecting VPCs]]
- [[Networking]]

## Flashcards
#flashcards

What is an ASN? :: The number that identifies an autonomous system (an independently run network)
BGP vs OSPF? :: BGP routes between ASes based on policies. OSPF finds shortest paths inside one AS
Where does an ASN appear in AWS? :: Transit gateway settings, VPN and Direct Connect (BGP sessions)
