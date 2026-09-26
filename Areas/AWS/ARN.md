---
type: concept
created: 2026-09-20
topic: AWS
confidence: 1
tags: [aws]
---
# ARN

> [!abstract] In one sentence
> An **ARN (Amazon Resource Name)** is the globally unique "full address" of any AWS resource, used whenever AWS needs to point at one exact thing, especially in [[IAM]] policies.

## The format

```
arn:partition:service:region:account-id:resource
```

| Part | Example | Note |
|---|---|---|
| partition | `aws` | `aws-cn` for China, `aws-us-gov` for GovCloud |
| service | `s3`, `ec2`, `iam`, `lambda` | |
| region | `eu-west-1` | **Empty** for global services (IAM, S3 buckets) |
| account-id | `123456789012` | Empty for S3 buckets (bucket names are globally unique) |
| resource | `instance/i-0abc…` | Format depends on the service |

## Examples
```
arn:aws:iam::123456789012:user/alice                        ← IAM user (no region)
arn:aws:s3:::my-bucket                                      ← S3 bucket (no region, no account)
arn:aws:s3:::my-bucket/*                                    ← every object in it
arn:aws:ec2:eu-west-1:123456789012:instance/i-0abcd1234
arn:aws:lambda:eu-west-1:123456789012:function:my-function
arn:aws:acm:us-east-1:123456789012:certificate/1234-abcd…   ← see ACM
```

## Why it matters
- IAM policies use ARNs in `"Resource"` to say *which* things a permission applies to
- Wildcards: `arn:aws:s3:::my-bucket/*` = all objects in the bucket
- Resource **IDs** (`i-0abc…`, `vpc-…`) are only unique inside an account/region. **ARNs are unique everywhere**

## Connects to
- [[IAM]]: every user/role has an ARN, and policies target ARNs
- [[CloudTrail]]: logs show the ARN of who acted and on what
- [[VPC]]: resource ID prefixes (`vpc-`, `subnet-`, `sg-`…)
- [[Certificate Manager (ACM)]]: certificates are picked by ARN in CLI/IaC

## Flashcards
#flashcards

ARN format? :: arn:partition:service:region:account-id:resource
Why does an S3 bucket ARN have no region or account? :: Bucket names are globally unique
ARN for all objects in bucket `photos`? :: arn:aws:s3:::photos/*
