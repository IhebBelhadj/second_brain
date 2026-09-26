---
type: compare
created: 2026-09-26
topic: AWS
confidence: 1
tags: [aws, compute]
---
# EC2 vs Lightsail vs Lambda

> [!abstract] The short answer
> **Lightsail** when I want a simple server and a fixed bill. **EC2** when I need control (networking, scaling, instance types). **Lambda** when my code only needs to run when something happens.

## Side by side

| | [[Lightsail]] | [[EC2]] | [[Lambda]] |
|---|---|---|---|
| What I get | A server bundle | A raw virtual machine | A function |
| I manage | OS, app | OS, app, network, scaling | Just the code |
| Pricing | Fixed monthly plan | Per second, plus EBS, IPs, data… | Per request + duration |
| Idle cost | Full price | Full price (if running) | **Zero** |
| Scaling | Manual (bigger plan, more instances + LB) | [[Auto Scaling]] | Automatic, built in |
| Networking | Hidden VPC, simple firewall | Full [[VPC]] control | AWS network by default, VPC optional |
| Max run time | Forever | Forever | 15 minutes |
| Console | Separate, very simple | EC2 console | Lambda console |
| Typical use | WordPress, small site, dev box | Production apps, custom setups | APIs, event processing, cron jobs |

## What they share
- They all run **my code on AWS compute**. Lightsail is EC2 underneath, and Lambda runs on AWS-managed servers too
- All can sit behind a domain with [[Route 53]] and serve HTTPS (Lightsail with its own certs, the others with [[Certificate Manager (ACM)|ACM]])

## Where they actually differ
**How much AWS makes me think about**:
```
more control, more work ◄───────────────────────────► less control, less work
        EC2                    Lightsail                     Lambda
  (I build everything)   (AWS pre-packages it)   (I don't even see a server)
```

And the **links between them**:
- Lightsail → EC2: **snapshot export** is the upgrade path when I outgrow Lightsail
- EC2 ↔ Lambda: both can be targets of the same ALB **target group** types ([[Load balancers]]), so an app can mix them
- Lambda can react to things EC2 does (via EventBridge), e.g. "an instance was stopped"

## If you have to choose
- A personal blog / portfolio, want it running in 10 minutes → **Lightsail**
- Traffic is spiky or rare, code is short-lived → **Lambda**
- Need private subnets, load balancing + auto scaling, specific instance types, long-running processes → **EC2**
- Started on Lightsail and now need auto scaling → **export to EC2**

## Flashcards
#flashcards

Which of EC2 / Lightsail / Lambda costs nothing when idle? :: Lambda
Which one has a fixed monthly price? :: Lightsail
How do you move from Lightsail to EC2? :: Snapshot → export to EC2 → AMI → launch instance
A job runs for 2 hours: Lambda or EC2? :: EC2 (or containers). Lambda's max is 15 minutes
