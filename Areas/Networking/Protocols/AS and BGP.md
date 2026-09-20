---
type: note
created: 2026-09-20
topic:
tags: []
---
# AS and BGP

> BGP (**Border Gateway Protocol**) is the routing protocol behind the internet network which is an interconnected mesh of smaller managed networks which all manage their internal routing. Thus the need for a decentralised protocol that manages the communication between these systems ,lets call them **Autonomous Systems** (AS)  where each has its own **Autonomous System Number** 

### BGP vs OSPF 

One important question to ask is why would you need this BGP protocol when you have a routing protocol for shortest path like OSPF ? 

To answer that we might need to look at the needs of the internet in today's world. While OSPF delivers when it comes to shortest paths resolution, there is no way to encode custom policies and biases into it which is what is very needed in today's relationship between multiple autonomous systems each managing their own connections and routings and each have biases when it comes to routing you to a destination based on policies or cost optimisation. Thus BGP is born

But when you look closer you can see that autonomous systems themselves implement internal OSPF routing to resolve shortest route paths within their networks  

```
                    INTERNET
                       │
          ┌────────────┴────────────┐
          │          BGP             │
          ▼                          ▼
       AS 100                      AS 200
    ┌─────────┐                  ┌─────────┐
    │         │                  │         │
    │ OSPF    │                  │ OSPF    │
    │         │                  │         │
    └─────────┘                  └─────────┘
      internal                     internal
       routing                      routing
```
