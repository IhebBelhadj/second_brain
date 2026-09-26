---
type: concept
created: 2026-09-26
topic: AWS
confidence: 1
tags: [aws, security]
---
# AWS WAF

> [!abstract] In one sentence
> WAF (**Web Application Firewall**) inspects **HTTP requests** before they reach my app and blocks the bad ones: SQL injection, XSS, known bad bots, too many requests from one IP…

## Sub-services & features

> Everything this service contains, grouped the way the console's left menu groups it. Linked = I have a note on it.

WAF shares a console with Shield and Firewall Manager (**WAF & Shield**). The console was redesigned in 2025, so some names differ (e.g. web ACLs can appear as **protection packs**).

| Area | Sub-feature | What it's for |
|---|---|---|
| **AWS WAF** | Web ACLs / protection packs | The rule sets attached to ALB, CloudFront, API Gateway… |
| | Rule groups | My reusable groups of rules |
| | AWS managed rules | Ready-made: core rule set, SQL injection, known bad inputs, IP reputation… |
| | Marketplace managed rules | Rule sets sold by security vendors |
| | IP sets / Regex pattern sets | Reusable lists referenced by rules |
| | Bot Control | Detect and manage bots (paid add-on) |
| | Fraud Control | Account takeover / fake account creation protection (paid add-on) |
| | CAPTCHA / Challenge | Make suspicious clients prove they're human/browsers |
| | Application integration SDKs | Client-side tokens for web/mobile apps |
| | Logging & metrics | Full request logs to CloudWatch Logs / S3 / Firehose, sampled requests |
| **AWS Shield** | Standard (free, automatic) / Advanced (paid) | DDoS protection. Advanced adds a response team + cost protection |
| **Firewall Manager** | Security policies | Push WAF/Shield/security group rules across all accounts of an [[AWS Organizations\|organization]] |

## In my own words

*Starter note, to fill in when I study it properly.*

A [[EC2#Security groups|security group]] only sees IPs and ports ("port 443 open"). It has no idea *what's inside* the request. WAF works at **Layer 7**: it reads the URL, headers, body, and decides.

- **Web ACL**: the list of rules I attach to a resource
- **Rules**: e.g. "block if the body looks like SQL injection", "block IPs from this list", "max 100 requests per 5 minutes per IP" (**rate-based rule**)
- **Managed rule groups**: ready-made rule sets from AWS (common attacks, known bad inputs, bot control…), so I don't write everything myself
- Each rule: **Allow / Block / Count** (Count = just watch, handy for testing a rule before enforcing it)

## Where it plugs in

WAF doesn't stand alone. It attaches to something that receives HTTP:

```
User ──► CloudFront ──► ALB ──► app
          ▲ WAF         ▲ WAF
```

- [[Load balancers|Application Load Balancer]]
- CloudFront
- API Gateway
- AppSync, Cognito, App Runner…

**Not** on an NLB (that one doesn't understand HTTP) and not directly on EC2.

## Related
- **Shield**: DDoS protection. Standard is free and automatic. WAF handles the application-level stuff
- [[Certificate Manager (ACM)]]: HTTPS on the same ALB/CloudFront

## Connects to
- [[Load balancers]]
- [[How AWS services connect]]

## Flashcards
#flashcards

What layer does WAF work at? :: Layer 7 (HTTP)
Name three things WAF can attach to :: ALB, CloudFront, API Gateway
How do you block an IP that sends too many requests? :: A rate-based rule in the web ACL
Security group vs WAF? :: SG filters IPs/ports (L3/L4). WAF inspects the HTTP request content (L7)

## Links
- [What is AWS WAF? (docs)](https://docs.aws.amazon.com/waf/latest/developerguide/what-is-aws-waf.html)
