---
type: concept
created: 2026-09-26
topic: AWS
confidence: 1
tags: [aws, security, https]
---
# Certificate Manager (ACM)

> [!abstract] In one sentence
> ACM gives me **free TLS/SSL certificates** (the thing behind the 🔒 in the browser) and **renews them automatically**, but only for AWS services that can hold them, like load balancers and CloudFront.

## In my own words

To serve `https://myapp.com`, the server has to show the browser a certificate saying "I really am myapp.com", signed by an authority the browser trusts. Normally you buy one or use Let's Encrypt, then install it and remember to renew it.

With ACM:
- I ask for a certificate for `myapp.com` (and `*.myapp.com`)
- I prove I own the domain
- AWS issues it, keeps the private key safe, and **renews it forever** as long as my proof stays in place
- I attach it to my load balancer with a dropdown

The catch: **I never get the private key** (for the normal free certs), so I can't copy it onto an EC2 instance and run nginx with it. The certificate lives on the **load balancer**, which is exactly why HTTPS is usually "terminated" at the ALB.

> [!note] AWS added a paid "exportable" public certificate option in 2025 for the cases where you really need the cert on your own server. The classic free cert stays inside AWS.

## Proving I own the domain

| Method | How | Verdict |
|---|---|---|
| **DNS validation** ✅ | ACM gives me a CNAME record to add to my DNS | Recommended. Renewal is automatic as long as the CNAME stays |
| **Email validation** | ACM emails admin@myapp.com etc. | Annoying, and renewals need clicking again |

If my domain is in [[Route 53]], DNS validation is a single **"Create records in Route 53"** button.

## Console walkthrough

> [!note] The ACM docs have no console screenshots. The steps are written out; I'll add my own screenshots when I do it.

1. **Switch to the right region first!** (see the trap below)
2. **Certificate Manager → Request a certificate → Request a public certificate**
3. Domain names:
   - `myapp.com`
   - `*.myapp.com` (wildcard: covers `www`, `api`… but **only one level deep**)
4. Validation method: **DNS validation**
5. Key algorithm: RSA 2048 is fine
6. **Request**. Status is now **Pending validation**
7. Open the certificate → **Create records in Route 53** → Create
8. After a few minutes, status → **Issued** ✅
9. Go to **EC2 → Load balancers → my ALB → Listeners → Add listener**
   - Protocol **HTTPS**, port **443** → forward to my target group
   - Default SSL certificate: **From ACM** → pick the one I just made
10. Edit the **HTTP :80** listener → **Redirect to HTTPS :443**, so nobody stays on plain HTTP

```
Browser ──HTTPS:443──► ALB (ACM cert here) ──HTTP:8080──► EC2 instances
         encrypted      "TLS termination"      inside the VPC
```

## Connects to
- [[Route 53]]: DNS validation records, one click
- [[Load balancers]]: the ALB's HTTPS listener is where the cert goes (NLB TLS listeners too)
- CloudFront: works too, but the cert **must be in `us-east-1`**
- API Gateway: custom domain names use ACM certs
- [[Lightsail]]: doesn't use ACM directly. Lightsail load balancers / distributions have their **own** free certificates
- [[EC2]]: **not directly**. Put an ALB in front
- Big picture → [[How AWS services connect]]

## Easy to get wrong
- **Region matters.** A certificate for an ALB in `eu-west-1` must be requested in `eu-west-1`. For **CloudFront it's always `us-east-1`**. Classic exam trap
- `*.myapp.com` does **not** cover `myapp.com` itself → add both names
- `*.myapp.com` does **not** cover `a.b.myapp.com`
- Deleting the validation CNAME = the certificate silently fails to renew later
- Public ACM certs are free. **Private CA** (for internal certs) is a separate, paid thing

## Flashcards
#flashcards

What does ACM do? :: Issues free public TLS certificates and renews them automatically for integrated AWS services
Can I install a standard ACM public certificate directly on an EC2 instance? :: No. The private key isn't exportable. Put an ALB (or CloudFront) in front and attach the cert there
Which region must an ACM certificate be in for CloudFront? :: us-east-1 (N. Virginia)
Which region for an ALB certificate? :: The same region as the ALB
Best validation method and why? :: DNS validation, because renewals are automatic as long as the CNAME record stays
Does `*.myapp.com` cover `myapp.com`? :: No, request both names on the certificate

## Links
- [Requesting a public certificate (docs)](https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-public.html)
- [DNS validation](https://docs.aws.amazon.com/acm/latest/userguide/dns-validation.html)
- [Services integrated with ACM](https://docs.aws.amazon.com/acm/latest/userguide/acm-services.html)
