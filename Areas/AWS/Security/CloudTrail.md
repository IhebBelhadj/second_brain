---
type: concept
created: 2026-09-20
topic: AWS
confidence: 1
tags: [aws, security, governance]
---
# CloudTrail

> [!abstract] In one sentence
> CloudTrail records **every API call** made in my AWS account (who did what, on which resource, from where, when), whether it came from the console, the CLI, an SDK, or another AWS service.

## In my own words

*Starter note.*

Every click in the console is really an API call (`RunInstances`, `CreateBucket`, `DeleteUser`…). CloudTrail writes each one down:

```
IAM Role:  AppRole
Action:    s3:GetObject
Resource:  arn:aws:s3:::my-bucket/file.txt
Time:      14:32
Source IP: ...
```

- **Event history**: the last **90 days** of management events, free, on by default
- **Trail**: to keep logs longer, I create a trail that delivers them to an **S3 bucket** (optionally to CloudWatch Logs for alerts)
- **Organization trail**: one trail for all accounts in [[AWS Organizations]]
- **Management events** (creating/changing resources) are logged by default. **Data events** (e.g. every S3 `GetObject`, every Lambda invoke) must be turned on, and cost extra

## Why it matters
- "Who deleted the production database?" → CloudTrail
- Security investigations, compliance audits
- Alerts: CloudTrail → CloudWatch → alarm when someone logs in as root

## CloudTrail vs the others
| Tool | Answers |
|---|---|
| **CloudTrail** | Who did **what API call**, when |
| IAM **Access Advisor** | When was a **service** last used by this principal (see [[IAM]]) |
| **CloudWatch** | How are my resources **performing** (metrics, app logs) |
| **Config** | What did a resource's **configuration** look like over time |

## Connects to
- [[IAM]]: every action by a user/role is recorded
- [[AWS Organizations]]: organization trail
- [[Bastion host]]: Session Manager sessions show up here
- [[Lambda]]: function changes are management events. Invocations are data events

## Flashcards
#flashcards

How long is CloudTrail event history kept by default? :: 90 days
How do you keep CloudTrail logs longer? :: Create a trail that delivers to an S3 bucket
CloudTrail vs CloudWatch? :: CloudTrail is who did which API call. CloudWatch is metrics and logs about how things run
Are S3 object reads logged by default? :: No, those are data events and must be enabled on a trail

## Links
- [What is AWS CloudTrail? (docs)](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html)
