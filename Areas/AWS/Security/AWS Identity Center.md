---
type: concept
created: 2026-09-21
topic: AWS
confidence: 1
tags: [aws, security]
---
# AWS Identity Center

> [!abstract] In one sentence
> **IAM Identity Center** (formerly AWS SSO) gives a person **one login** that opens the door to **many AWS accounts**, each with the right level of access.

## Sub-services & features

> Everything this service contains, grouped the way the console's left menu groups it. Linked = I have a note on it.

| Menu | Sub-feature | What it's for |
|---|---|---|
| **Dashboard** | | Setup checklist + the **AWS access portal URL** |
| **Users / Groups** | | People (when Identity Center is the identity source) |
| **Settings** | Identity source | Built-in directory, **Active Directory**, or an **external IdP** (Entra ID, Okta, Google…) with SCIM sync |
| | Authentication | MFA rules, session duration |
| **Multi-account permissions** | AWS accounts | Assign user/group + permission set to accounts |
| | Permission sets | Reusable permission bundles → become IAM roles |
| **Application assignments** | Applications | SSO into apps (Salesforce, Slack, custom SAML apps, AWS apps like QuickSight) |
| | Trusted token issuers | Let external tokens be exchanged for AWS access |
| **AWS access portal** | *(for users)* | Where people log in and pick an account + role, and get CLI credentials |

## In my own words

*Starter note, to fill in once I actually set it up.*

The problem: in an [[AWS Organizations|organization]] with 10 accounts, creating an [[IAM]] user in each account for each person is painful and insecure (10 passwords, keys everywhere).

Identity Center fixes it:
1. People live in **one place**: Identity Center's own directory, or an external one (Microsoft Entra ID, Google Workspace, Okta…)
2. I define **permission sets** ("ReadOnly", "Admin"…), which are basically reusable policy bundles
3. I assign: *user/group* + *account* + *permission set*
4. The user logs into the **AWS access portal**, sees the accounts they're allowed into, and clicks one. Behind the scenes, Identity Center creates an **IAM role** in that account and the user assumes it, with **temporary credentials**

```
Alice ──login──► AWS access portal
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
      Prod acct   Dev acct   Security acct
      ReadOnly    Admin      (not assigned)
```

## Why it matters
- No long-term passwords/keys per account → safer
- Offboarding = disable one user, not 10
- It's what AWS recommends today for **humans**. IAM users are mostly legacy for people

## Connects to
- [[AWS Organizations]]: works across the org's accounts
- [[IAM]]: permission sets become IAM roles in each account
- [[CloudTrail]]: logins and role assumptions are logged

## Flashcards
#flashcards

What is a permission set? :: A reusable set of permissions that becomes an IAM role in each account it's assigned to
IAM user vs Identity Center user for a person? :: Identity Center: one identity, temporary credentials, many accounts

## Links
- [What is IAM Identity Center? (docs)](https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html)
