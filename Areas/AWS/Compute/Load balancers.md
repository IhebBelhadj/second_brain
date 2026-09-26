---
type: concept
created: 2026-09-24
topic: AWS
confidence: 2
tags: [aws, compute, networking]
---
# Load balancers

> [!abstract] In one sentence
> A load balancer is the single front door for my app: it receives all the traffic and spreads it across the healthy servers (the **targets**) behind it.

> [!question] Are load balancers part of EC2?
> Sort of. **Elastic Load Balancing (ELB)** is technically its own service, but its console lives **inside the EC2 console** (left menu → Load Balancing → Load Balancers / Target Groups). That's why I thought it was part of EC2.

## Types of load balancers

![[Pasted image 20260924195606.png]]

AWS has **four** of them. What matters is **what kind of traffic they understand** and so how smart their routing can be:

| Load balancer | Layer | Protocols | Typical use |
|---|---|---|---|
| **Application (ALB)** | L7 | HTTP/HTTPS | Websites, REST APIs, microservices |
| **Network (NLB)** | L4 | TCP/UDP/TLS | High performance, low latency, static IPs |
| **Gateway (GWLB)** | L3 | IP packets | Sending traffic through firewalls / IDS appliances |
| **Classic (CLB)** | L4/L7 | TCP/HTTP/HTTPS | Legacy. Don't use for new stuff |

> [!tip] The one-liner
> **ALB = "I understand your HTTP request."**
> **NLB = "I understand your network connection."**

## Application Load Balancer (ALB)

It works at **Layer 7**, so it can read the HTTP request (path, host, headers) and route on it:

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

It's the load balancer I'll meet the most as a developer: websites, REST APIs, HTTP microservices, containers (ECS), anything needing path/host-based routing.

### Setting up an ALB

![[Pasted image 20260924200600.png]]

![[Pasted image 20260924202521.png]]

- **Network mapping**: pick the right [[VPC]] and select subnets in the AZs where my instances are (at least two AZs). An internet-facing ALB goes in **public subnets**, and the instances can stay private
- **Listeners and routing**: a listener = protocol + port (e.g. HTTPS :443). Each listener forwards to a **target group**

![[Pasted image 20260924201513.png]]

![[Pasted image 20260924202108.png]]

- For **HTTPS**, the listener needs a certificate → from [[Certificate Manager (ACM)]]. Then add an HTTP :80 listener that **redirects to 443**
- To protect it, attach [[AWS WAF]] rules to the ALB
- To give it a nice name, create an **Alias** record in [[Route 53]]

## Target groups

> A **target group** is the list of destinations (EC2 instances, IPs, Lambda functions) that a load balancer can send traffic to, **plus how to check that they're healthy**.

Why a separate thing? It separates concerns: the **load balancer** only decides *where traffic goes* (listeners, rules), and the **target group** handles *who is in the pool and who is healthy*. That's also what lets [[Auto Scaling]] plug in: the ASG adds/removes instances in the target group, and the ALB never needs to know.

![[Pasted image 20260924194236.png]]

| Target type | Example |
|---|---|
| **Instance** | [[EC2]] instances |
| **IP** | Private IPs, often containers, or servers on-premises |
| **Lambda** | A [[Lambda]] function |
| **ALB** | An ALB behind an NLB (when I need static IPs *and* HTTP routing) |

```
                     ┌── EC2 Instance A : port 8080
Internet             │
   │                 │
   ▼                 ▼
Application  →  Target Group
Load Balancer        ▲
   (ALB)             │
                     └── EC2 Instance B : port 8080

Listener:  HTTPS :443  ──►  forward to my-app-tg
```

### Health checks (important!)

The target group regularly calls each target:
```
http://EC2-A:8080/health
http://EC2-B:8080/health
```
If one stops answering correctly, it's marked **unhealthy** and the load balancer stops sending it traffic until it recovers. With Auto Scaling + ELB health checks, the unhealthy instance even gets **replaced**.

![[Pasted image 20260924195037.png]]

Newly registered instances show as **pending** at first. Here's the target group page:
![[Pasted image 20260924195127.png]]

![[Pasted image 20260924195206.png]]

The health status says **unused** here because no load balancer uses this target group yet. Health checks only run once a load balancer points to it.

### Load balancing strategy
> [!note] The algorithm is set **on the target group**, not on the load balancer.

1. **Round robin**: each target in turn
2. **Least outstanding requests**: the target with the fewest requests in progress
(3. **Weighted random**, a newer option, which I haven't looked at yet)

## Network Load Balancer (NLB)

It deals with **connections** (TCP/UDP), not HTTP meaning. So it can't route on `/api`, but it's very fast.

Use it for:
- TCP/UDP traffic, protocols other than HTTP (game servers, MQTT, databases…)
- Very high throughput / very low latency
- **Static IPs / Elastic IPs**, when a client needs to whitelist an IP
- TLS pass-through

## Connects to
- [[EC2]]: the usual targets
- [[Auto Scaling]]: registers/deregisters instances in target groups
- [[Lambda]]: can be a target
- [[Certificate Manager (ACM)]]: certificates for HTTPS listeners
- [[Route 53]]: Alias record → ALB
- [[AWS WAF]]: attached to the ALB
- [[VPC]]: lives in subnets of a VPC, across AZs
- [[Lightsail]]: has its own simpler load balancer
- Big picture → [[How AWS services connect]]

## Easy to get wrong
- ALB = HTTP only. For raw TCP/UDP → NLB
- The routing algorithm is on the **target group**
- "Unused" health status = no load balancer is attached to that target group yet
- The app's security group should allow traffic **from the ALB's security group**, not from the whole internet

## Flashcards
#flashcards

ALB vs NLB in one line each? :: ALB is Layer 7 and understands HTTP (paths, hosts). NLB is Layer 4, handles TCP/UDP connections, very fast, static IPs
Where is the load balancing algorithm configured? :: On the target group
What are the target types of a target group? :: Instance, IP, Lambda, ALB
Why does a target group show "unused" health? :: No load balancer is forwarding to it yet
Which load balancer do you need for static IPs? :: NLB
Where does the HTTPS certificate go? :: On the ALB listener (from ACM)
