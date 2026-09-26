---
type: concept
created: 2026-09-26
topic: AWS
confidence: 1
tags: [aws, networking, dns]
---
# Route 53

> [!abstract] In one sentence
> AWS's DNS service: it turns `myapp.com` into the address of my load balancer / server. It can also **register domains** and **health-check** endpoints to route around failures.

(The name comes from **port 53**, the port DNS runs on.)

## Sub-services & features

> Everything this service contains, grouped the way the console's left menu groups it. Linked = I have a note on it.

| Menu group | Sub-service | What it's for |
|---|---|---|
| **Dashboard** | | Quick links: register domain, create zone… |
| **Hosted zones** | Public / private hosted zones | The DNS records of my domains (see below) |
| | DNSSEC signing | Cryptographically sign my zone against DNS spoofing |
| **Health checks** | Health checks | Monitor endpoints, used by failover routing and CloudWatch alarms |
| **Traffic flow** | Traffic policies / policy records | A visual editor to combine routing policies (e.g. latency *then* failover) |
| **IP-based routing** | CIDR collections | Lists of client IP ranges for IP-based routing |
| **Profiles** | Profiles | Share DNS config (private zones, resolver rules) across VPCs/accounts |
| **Domains** | Registered domains / requests | Buy, renew and transfer domains |
| **Resolver** | VPCs | The built-in DNS server of every VPC (`.2` address) |
| | Inbound / outbound endpoints + rules | **Hybrid DNS**: on-prem ↔ VPC name resolution |
| | Query logging | Log DNS queries made from my VPCs |
| **DNS Firewall** | Rule groups, domain lists | Block lookups of malicious domains from my VPCs |
| **Application Recovery Controller** | *(now its own console)* | Readiness checks + routing controls for multi-region failover |

## How DNS works (and where Route 53 fits)

![[aws-docs route53 how dns routes.png]]
*From the AWS docs*

1. I type `www.example.com`
2. My DNS resolver (usually my ISP) doesn't know it, so it asks around:
3. **Root name server** → "ask the `.com` servers"
4. **`.com` name server** → "ask Route 53's name servers for example.com"
5. **Route 53** → "it's `192.0.2.44`"
6. The resolver gives me the IP (and caches it for the **TTL**)
7. My browser talks to that IP directly

So Route 53 is the **last stop**: the authority that actually knows the answer for my domain.

## The pieces

| Piece | What it is |
|---|---|
| **Hosted zone** | A container for all the DNS records of one domain (`myapp.com`). Costs a little per month |
| **Public hosted zone** | Answers for the whole internet |
| **Private hosted zone** | Only answers inside the [[VPC]]s I attach it to (e.g. `db.internal`) |
| **Record** | One line: name → type → value |
| **Domain registration** | Buying the domain itself. Route 53 can do it, and creates the hosted zone for me |
| **Health check** | Pings an endpoint. Can take unhealthy ones out of DNS answers |

### Record types I actually need
| Type | Points to | Example |
|---|---|---|
| **A** | IPv4 address | `myapp.com → 3.120.10.5` |
| **AAAA** | IPv6 address | |
| **CNAME** | Another name | `www.myapp.com → myapp.com` |
| **MX** | Mail server | |
| **TXT** | Any text (ownership proofs, SPF) | |
| **NS** | The name servers for the zone | Created automatically |
| **Alias** ⭐ | An AWS resource | `myapp.com → my-alb-123.eu-west-1.elb.amazonaws.com` |

> [!tip] Alias records are the AWS superpower
> An Alias is an A/AAAA record that points to an **AWS resource** (ALB, CloudFront, S3 website, API Gateway…) instead of an IP.
> - Load balancer IPs **change all the time**, so I can't hardcode an A record → Alias follows them automatically
> - Unlike a CNAME, an Alias works on the **root domain** (`myapp.com`, not just `www.myapp.com`)
> - Alias queries to AWS resources are free

## Routing policies

When I create a record I pick *how* Route 53 answers:

| Policy | What it does | Use it when |
|---|---|---|
| **Simple** | One answer, always | One server / one ALB |
| **Weighted** | 80% → A, 20% → B | Canary releases, A/B tests |
| **Latency** | Sends the user to the region with the lowest latency | App deployed in several regions |
| **Failover** | Primary, and secondary only if the primary health check fails | Disaster recovery |
| **Geolocation** | Based on the user's country/continent | Legal/language reasons |
| **Geoproximity** | Based on distance, with a "bias" knob | Shift traffic between regions gradually |
| **Multivalue answer** | Returns several healthy IPs | Poor man's load balancing |
| **IP-based** | Based on the user's IP range | Route specific ISPs/networks |

## Console walkthrough: point my domain at a load balancer

> [!note] The AWS docs for Route 53 have no console screenshots. The steps below are written out; I'll paste my own screenshots here the next time I do it.

1. **Route 53 → Hosted zones → Create hosted zone**
   - Domain name: `myapp.com`, Type: **Public hosted zone**
   - AWS creates **NS** and **SOA** records automatically
2. *If the domain was bought somewhere else* (Namecheap, OVH…): copy the 4 **NS** values into the registrar's name server settings. Otherwise nobody on the internet will ever ask Route 53
3. **Create record**
   - Record name: leave empty (root) or `www`
   - Record type: **A**
   - Turn on the **Alias** toggle
   - Route traffic to: **Alias to Application and Classic Load Balancer** → region → pick my ALB
   - Routing policy: **Simple**
4. Wait a minute, then `dig myapp.com` or `nslookup myapp.com` to check

## Connects to
- [[Load balancers]]: the usual target, through an Alias record
- [[Certificate Manager (ACM)]]: ACM proves I own the domain with a CNAME record. If the zone is in Route 53, it's a single **"Create records in Route 53"** button
- [[Lightsail]]: Lightsail has its **own** DNS zones (simpler, free), but I can use Route 53 instead
- [[EC2]]: point an A record at an **Elastic IP** (a plain public IP changes on stop/start)
- [[VPC]]: private hosted zones give internal names to resources inside the VPC
- CloudWatch: health checks can trigger alarms
- Big picture → [[How AWS services connect]]

## Easy to get wrong
- Creating a hosted zone does **nothing** until the registrar points to its NS records
- **CNAME at the root domain is not allowed** (DNS rule). Use an Alias
- DNS changes aren't instant for everyone, because resolvers cache answers for the TTL
- Route 53 is a **global** service: no region selector in the console

## Flashcards
#flashcards

What is a Route 53 hosted zone? :: A container for all DNS records of one domain
Why use an Alias record instead of an A record for an ALB? :: ALB IPs change. An Alias follows the resource automatically, works at the root domain, and is free
Can I use a CNAME for `myapp.com` (root)? :: No, CNAMEs aren't allowed at the zone apex. Use an Alias record
Which routing policy sends users to the closest-performing region? :: Latency-based routing
Which routing policy gives primary/backup behaviour? :: Failover (with a health check on the primary)
I created a hosted zone but the domain doesn't resolve. Why? :: The registrar's NS records don't point to the hosted zone's name servers yet

## Links
- [What is Amazon Route 53? (docs)](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html)
- [Routing traffic to an ELB load balancer](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-to-elb-load-balancer.html)
- [Choosing a routing policy](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html)
