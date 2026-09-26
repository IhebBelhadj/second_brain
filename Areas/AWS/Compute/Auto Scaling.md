---
type: concept
created: 2026-09-24
topic: AWS
confidence: 2
tags: [aws, compute]
---
# Auto Scaling

> [!abstract] In one sentence
> An **Auto Scaling group (ASG)** keeps the right number of [[EC2]] instances running: it replaces the ones that die, and adds or removes instances as traffic goes up and down, always staying between a **min** and a **max**.

## The three numbers

Every ASG has:
- **Min**: never go below this (e.g. 4)
- **Max**: never go above this (e.g. 12)
- **Desired**: what the ASG is aiming for *right now* (e.g. 6)

![[Pasted image 20260926092430.png]]

The rule that holds everything together: **Min ≤ Desired ≤ Max**

The ASG constantly compares *"how many healthy instances do I have?"* with *desired*, and launches or terminates instances to close the gap. **Scaling policies** move *desired* up and down (only between min and max).

## What it does for me (my summary of the docs)

| Feature | In plain words |
|---|---|
| **Health monitoring** | An instance dies or fails its health check → it gets replaced automatically |
| **Custom health checks** | I can define my own "is my app OK?" check |
| **Spread across AZs** | Instances are balanced across Availability Zones, so one data center going down doesn't take everything |
| **Mixed instance types** | Mix On-Demand and **Spot** (cheap but can be taken back) in one group to cut costs |
| **Spot replacement** | If AWS takes back a Spot instance, the ASG requests a new one. *Capacity Rebalancing* does it proactively |
| **Load balancer integration** | New instances are registered in the target group automatically, and removed ones are deregistered |
| **Instance refresh** | Rolling update when I change the AMI / launch template. Can be done as a canary (a few instances first) |
| **Lifecycle hooks** | Run something when an instance launches or before it's terminated (e.g. drain connections, save state) |
| **Scale-in protection** | Stop specific instances (e.g. running a long job) from being terminated on scale-in |

## How the pieces fit

The relationship between load balancer, target group and ASG, where **each one answers a different question**:

```
┌───────────────────────┐
│ ALB                   │
│ "Where should traffic │
│  go?"                 │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ Target Group          │
│ "Which targets are    │
│  available?"          │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ EC2 Instances         │
│ "Run my application"  │
└──────────┬────────────┘
           │
           ▲
┌──────────┴────────────┐
│ Auto Scaling Group    │
│ "How many instances   │
│  should exist?"       │
└───────────────────────┘
```

A real-world version of it:

```
                                  ┌──────────────────────┐
                                  │       INTERNET       │
                                  │   Users / Clients    │
                                  └──────────┬───────────┘
                                             │ HTTP / HTTPS
                                             ▼
                         ┌────────────────────────────────────┐
                         │   Application Load Balancer (ALB)  │
                         │   Listener :443 / :80              │
                         └────────────────┬───────────────────┘
                                          │ Forward
                                          ▼
                         ┌────────────────────────────────────┐
                         │          TARGET GROUP              │
                         │   Protocol: HTTP   Port: 8080      │
                         │   Health check: /health            │
                         └───────┬──────────┬──────────┬──────┘
                                 │          │          │
                         ┌───────▼───┐ ┌────▼──────┐ ┌─▼─────────┐
                         │ EC2 :8080 │ │ EC2 :8080 │ │ EC2 :8080 │
                         └─────▲─────┘ └────▲──────┘ └────▲──────┘
                               │            │             │
                    ┌──────────┴────────────┴─────────────┴──────┐
                    │          AUTO SCALING GROUP (ASG)          │
                    │  Min: 2        Desired: 3        Max: 10   │
                    └──────────────────────┬─────────────────────┘
                                           │ launches new instances from
                                           ▼
                              ┌─────────────────────────┐
                              │     LAUNCH TEMPLATE     │
                              │ AMI, instance type,     │
                              │ security group, IAM     │
                              │ role, user data, EBS    │
                              └─────────────────────────┘

        ┌────────────────────────────────────────────────────────────┐
        │ CLOUDWATCH: EC2 CPU / network, ALB request count…          │
        │   Scaling policy: "CPU > 70% → scale out"                  │
        │                   "CPU < 30% → scale in"                   │
        └──────────────────────┬─────────────────────────────────────┘
                               │ scaling decision
                               ▼
                        ASG: +1 / -1 EC2
```

> [!important] A scaling policy doesn't create instances itself
> ```
> Scaling policy → changes desired capacity
>   → ASG notices actual ≠ desired
>   → uses the launch template to create / terminate EC2 instances
>   → instances register / deregister in the target group
>   → ALB sends traffic only to the healthy ones
> ```

## Scaling policies

A **scaling policy** is the rule that tells the ASG *when* and *how* to change the number of instances:
```
IF average CPU utilization > 70% THEN increase capacity
```

The **policy belongs to the ASG**, but the **metric comes from CloudWatch**:
```
CloudWatch ──observes metrics──► Scaling policy ──"what should happen?"──► ASG ──► launch / terminate EC2
```

Types I've seen so far:
- **Target tracking**: "keep average CPU at 50%" (the easiest one, and AWS does the math)
- **Step / simple scaling**: "if CPU > 70%, add 2 instances"
- **Scheduled**: "every weekday at 8am, desired = 10"
- **Predictive**: learns from history and scales ahead of time

## Hands-on: my ASG setup

The architecture I built:

![[Pasted image 20260924204451.png]]

**1. Launch template first.** The ASG needs to know *how* to create an instance (see [[EC2]] → Launch templates):

![[Pasted image 20260924204403.png]]

When creating the template, there's a warning about the subnet. **Don't set a subnet in the template.** The ASG chooses the subnets itself:

![[Pasted image 20260924204543.png]]

Enable **auto-assign public IP** so each new instance gets a public IP (only needed because my instances are in public subnets for this exercise):

![[Pasted image 20260924204914.png]]

**2. The ASG creation form** (multi-step).

I can attach the load balancer here. It lists my existing target group, since the ALB already forwards to it (see diagram above):

![[Pasted image 20260924205033.png]]

![[Pasted image 20260924205226.png]]

> [!question] What is VPC Lattice?
> It showed up in this form. Short version: a newer service for **service-to-service networking** across VPCs and accounts at the HTTP level (routing, auth), without setting up peering or transit gateways. The ASG can register instances in a Lattice target group instead of an ELB one. <span style="color:rgb(192, 0, 0)">Still to study properly.</span>

![[Pasted image 20260924205344.png]]

**Health checks**: turn on **Elastic Load Balancing health checks**. Without this, the ASG only knows if the *VM* is alive. With it, it also replaces instances whose *app* fails the target group's health check:

![[Pasted image 20260924205449.png]]

**Group size and scaling**: this is where desired / min / max go, plus an optional scaling policy:

![[Pasted image 20260924205626.png]]

**Notifications**: push ASG events (instance launched, terminated, failed…) to an **SNS topic**, e.g. to get an email.

## Connects to
- [[EC2]]: launch templates, the instances themselves
- [[Load balancers]]: the target group is the meeting point
- [[VPC]]: the ASG spreads instances over subnets in several AZs
- CloudWatch: metrics that drive scaling policies
- SNS: notifications
- [[Lightsail]]: has **no** auto scaling, one of the main reasons to move to EC2
- [[Lambda]]: scales by itself, no ASG needed
- Big picture → [[How AWS services connect]]

## Easy to get wrong
- Setting a subnet in the launch template (the ASG wants to choose)
- Forgetting ELB health checks → the app is broken but the VM is "healthy", so nothing gets replaced
- Thinking the scaling policy launches instances. It only changes **desired**
- Desired can never go outside **min…max**

## Flashcards
#flashcards

What three numbers define an ASG's size? :: Min, desired, max, with Min ≤ Desired ≤ Max
What does a scaling policy actually change? :: The desired capacity. The ASG then launches/terminates instances to match
Where does the metric for a scaling policy come from? :: CloudWatch
What does the ASG need to know how to create instances? :: A launch template
Why enable ELB health checks on an ASG? :: So instances whose app fails the target group health check get replaced, not just dead VMs
How does an ASG work with an ALB? :: It registers/deregisters its instances in the ALB's target group
Easiest scaling policy type? :: Target tracking (e.g. keep average CPU at 50%)

## Links
- [What is Amazon EC2 Auto Scaling? (docs)](https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html)
- [AWS EC2 Auto Scaling: Step By Step Tutorial (Part 10), YouTube](https://www.youtube.com/watch?v=fwfkSxb1T-s&list=PL7iMyoQPMtAN4xl6oWzafqJebfay7K8KP&index=10)
