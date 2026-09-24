---
type: note
created: 2026-09-24
topic:
tags: []
---
# Load balancers

> Load balancers are part of the EC2 service (not sure if they are available else where or not , ==we will verify later ==)

## Types of load balancers 

![[Pasted image 20260924195606.png]]

AWS has **four main types of load balancers**. The important distinction is **what kind of traffic they understand and how they make routing decisions**

| Load Balancer                       | Layer     | Main protocol  | Typical use                                   |
| ----------------------------------- | --------- | -------------- | --------------------------------------------- |
| **Application Load Balancer (ALB)** | L7        | HTTP/HTTPS     | Web apps, REST APIs, microservices            |
| **Network Load Balancer (NLB)**     | L4        | TCP/UDP/TLS    | High-performance, low-latency network traffic |
| **Gateway Load Balancer (GWLB)**    | L3/L4-ish | IP traffic     | Firewalls, IDS/IPS, network appliances        |
| **Classic Load Balancer (CLB)**     | L4/L7     | TCP/HTTP/HTTPS | Legacy applications                           |
### Application Load Balancer — ALB

> The ALB operates at <span style="color:rgb(255, 192, 0)"><b>Layer 7</b></span>, meaning it understands HTTP.

```
                     ALB
                      │
          ┌───────────┼───────────┐
          │           │           │
       /api/*      /admin/*    /images/*
          │           │           │
          ▼           ▼           ▼
       API TG      Admin TG     Images TG
```

This is probably the **most common load balancer you'll encounter as a software engineer**

Its dead simple : 
a standard LB that you use typically when building: 
- websites
- REST APIs
- HTTP microservices
- containerized applications
- ECS services
- applications requiring path/host-based routing

#### ALB Setup 

![[Pasted image 20260924200600.png]]


### Network Load Balancer — NLB

> It deals with connections rather than understanding HTTP application semantics.

For example:

So has more specific use cases especially when routing traffic through different types of protocols other than HTTP

Use it when you want to achieve : 
- TCP/UDP load balancing
- very high throughput
- very low latency
- static IP addresses / Elastic IP support
- TLS pass-through or L4-style handling
- protocols other than HTTP

> <span style="color:rgb(255, 192, 0)">Note : </span>
> **ALB = "I understand your HTTP request."**  
> **NLB = "I understand your network connection."**

