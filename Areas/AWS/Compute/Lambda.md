---
type: concept
created: 2026-09-26
topic: AWS
confidence: 1
tags: [aws, compute, serverless]
---
# Lambda

> [!abstract] In one sentence
> I upload a function, AWS runs it **only when something triggers it** (an HTTP request, a file landing in S3, a message in a queue…), and I pay only for the milliseconds it runs. There's no server to manage.

## In my own words

With [[EC2]] I rent a machine that's on 24/7 whether anyone uses it or not, and I patch it, scale it and so on.
With Lambda I only give AWS **a function**:

```js
export const handler = async (event) => {
  return { statusCode: 200, body: "hello" };
};
```

- `event` = whatever triggered it (the HTTP request, the S3 file info, the SQS message…)
- AWS spins up a small environment, runs the function, and keeps it warm for a while in case another event comes
- 1,000 requests at once? AWS runs many copies in parallel. Scaling is automatic

## The limits worth knowing

| Thing | Value |
|---|---|
| Max run time | **15 minutes**. Longer jobs → ECS/Fargate, EC2, Step Functions |
| Memory | 128 MB → 10 GB. **CPU grows with memory** |
| Temp disk (`/tmp`) | Up to 10 GB, gone after the environment dies |
| Billing | Number of requests + (duration × memory) |
| Cold start | First call after idle is slower while the environment boots |

## Two kinds of permissions (confusing at first!)

```
         WHO CAN CALL ME?                 WHAT CAN I DO?
    ┌──────────────────────┐        ┌──────────────────────┐
    │ Resource-based policy│        │    Execution role    │
    │ "S3 / API Gateway is │───►λ───│ "I can write logs,   │
    │  allowed to invoke"  │        │  read this bucket…"  │
    └──────────────────────┘        └──────────────────────┘
```

- **Execution role**: an [[IAM]] role that the function *assumes*. By default it can only write logs to CloudWatch. If my function reads S3, I add that permission here
- **Resource-based policy**: who is allowed to *invoke* the function. The console adds it for me when I add a trigger

## Console walkthrough (screenshots from the AWS docs)

1. **Lambda → Create function → Author from scratch**
   - Name, **Runtime** (Node.js, Python…), Architecture (arm64 is cheaper)
   - Permissions: **Create a new role with basic Lambda permissions** (= logs only)
2. The code editor opens:

![[aws-docs lambda code editor.png]]

3. After changing code, **nothing is live until I click Deploy**:

![[aws-docs lambda deploy button.png]]

4. Test it without a real trigger: **create a test event** (a fake JSON `event`) and run it:

![[aws-docs lambda create test event.png]]

![[aws-docs lambda run test.png]]

5. Hook it to the real world: **Add trigger** in the function overview:

![[aws-docs lambda function overview trigger.png]]

6. Every `console.log` / `print` ends up in **CloudWatch Logs**, one log stream per environment:

![[aws-docs lambda log streams.png]]

### Example: react to files uploaded to S3

![[aws-docs lambda s3 trigger flow.png]]

Upload a file to the bucket → S3 fires an event → Lambda runs with the file name in `event` → logs go to CloudWatch. The execution role needs `s3:GetObject` on the bucket.

## What can trigger a Lambda

| Trigger | Typical use |
|---|---|
| API Gateway / **Function URL** | An HTTP API without servers |
| **[[Load balancers\|ALB]]** | A target group can have type **Lambda** (see the target types table in [[Load balancers]]) |
| S3 | Resize an image when it's uploaded |
| SQS / SNS | Process messages in the background |
| EventBridge | Cron-like schedules ("every night at 2am"), reacting to AWS events |
| DynamoDB Streams | React to data changes |

## Lambda and my VPC

By default a Lambda runs in **AWS's own network**, not in my [[VPC]]:
- ✅ It can reach the internet and public AWS APIs
- ❌ It **can't** reach my database in a private subnet

If it needs the DB → attach the function to my VPC (pick private subnets + a security group). But then:
- ❌ it **loses internet access**, unless the private subnet routes through a **NAT gateway**

```
Lambda (in VPC, private subnet) ──► RDS          ✅ same VPC
Lambda (in VPC, private subnet) ──► NAT GW ──► internet   ✅ needs NAT
```

## Connects to
- [[IAM]]: execution role + resource policy
- [[Load balancers]]: Lambda can be a target group target
- [[VPC]]: only when it needs private resources, and then NAT for internet
- [[Route 53]] + [[Certificate Manager (ACM)]]: a custom domain on API Gateway in front of Lambda
- [[CloudTrail]]: logs who changed/invoked functions (API calls). CloudWatch holds the function's own logs
- vs [[EC2]] and [[Lightsail]] → [[EC2 vs Lightsail vs Lambda]]
- Big picture → [[How AWS services connect]]

## Easy to get wrong
- Editing code in the console ≠ deployed. **Click Deploy**
- "Permission denied reading S3" → fix the **execution role**, not the trigger
- Lambda isn't good for long-running or always-on stuff (websockets servers, 1h jobs)
- Putting a Lambda in a VPC without NAT and wondering why `fetch()` to an external API times out

## Flashcards
#flashcards

Max execution time of a Lambda function? :: 15 minutes
How do you give a Lambda more CPU? :: Give it more memory. CPU scales with memory
Execution role vs resource-based policy? :: The execution role is what the function can do. The resource-based policy is who can invoke the function
Where do Lambda logs go? :: CloudWatch Logs (one log group per function)
My VPC-attached Lambda can reach RDS but not the internet. Why? :: VPC Lambdas have no internet access. The private subnet needs a route to a NAT gateway
Can an ALB send traffic to a Lambda? :: Yes, with a target group of type Lambda

## Links
- [Getting started (docs, with screenshots)](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html)
- [Tutorial: S3 trigger](https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html)
- [Lambda with an ALB](https://docs.aws.amazon.com/lambda/latest/dg/services-alb.html)
