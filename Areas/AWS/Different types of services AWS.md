---
type: note
created: 2026-09-19
topic: AWS
tags: []
---
# Types of AWS services

| Type                    | Service                        | What it does                                                               |
| ----------------------- | ------------------------------ | -------------------------------------------------------------------------- |
| **Compute**             | EC2                            | Virtual machines you size, patch and scale yourself ==see link== : [[EC2]] |
|                         | Lambda                         | Runs your code on demand, no servers to manage, billed per request         |
|                         | EC2 Auto Scaling               | Adds and removes instances automatically to match demand                   |
|                         | Elastic Beanstalk              | Takes your code and provisions the whole stack for you                     |
|                         | Batch                          | Queues and runs batch jobs across managed compute                          |
|                         | Lightsail                      | Simplified virtual server with fixed monthly pricing                       |
|                         | App Runner                     | Runs a container or repo as a scaled web service, zero setup               |
| **Containers**          | ECS                            | AWS's own container orchestrator                                           |
|                         | EKS                            | Managed Kubernetes                                                         |
|                         | Fargate                        | Serverless engine for ECS/EKS — no EC2 instances to manage                 |
|                         | ECR                            | Private registry for container images                                      |
| **Storage**             | S3                             | Object storage, effectively unlimited, accessed by key                     |
|                         | EBS                            | Block volumes attached to one EC2 instance at a time                       |
|                         | EFS                            | Shared filesystem many instances can mount at once                         |
|                         | FSx                            | Managed third-party filesystems (Windows, Lustre, NetApp, OpenZFS)         |
|                         | S3 Glacier                     | Cheap archival tiers for data you rarely retrieve                          |
|                         | Storage Gateway                | Bridge giving on-premises systems access to AWS storage                    |
|                         | AWS Backup                     | Central backup scheduling and policy across services                       |
|                         | Snow Family                    | Physical devices for moving data too big for the network                   |
| **Database**            | RDS                            | Managed relational databases (PostgreSQL, MySQL, Oracle, SQL Server…)      |
|                         | Aurora                         | AWS's own MySQL/PostgreSQL-compatible engine, faster and more resilient    |
|                         | DynamoDB                       | Serverless NoSQL key-value store with millisecond latency                  |
|                         | ElastiCache                    | Managed in-memory cache (Redis/Valkey or Memcached)                        |
|                         | MemoryDB                       | Durable in-memory database, Redis-compatible                               |
|                         | Redshift                       | Columnar data warehouse for analytics over huge datasets                   |
|                         | DocumentDB                     | MongoDB-compatible document database                                       |
|                         | Neptune                        | Graph database for highly connected data                                   |
|                         | Timestream                     | Purpose-built time-series database                                         |
|                         | Keyspaces                      | Managed Cassandra-compatible database                                      |
| **Networking**          | VPC                            | Your private virtual network: subnets, routing, gateways                   |
|                         | Route 53                       | DNS, domain registration, and health-checked traffic routing               |
|                         | CloudFront                     | CDN that caches content at edge locations worldwide                        |
|                         | Elastic Load Balancing         | Spreads incoming traffic across targets (ALB, NLB, GWLB)                   |
|                         | API Gateway                    | Front door for APIs — auth, throttling, routing to backends                |
|                         | NAT Gateway                    | Lets private subnets reach the internet outbound only                      |
|                         | Direct Connect                 | Dedicated private line from your datacentre to AWS                         |
|                         | Site-to-Site VPN               | Encrypted tunnel to your VPC over the public internet                      |
|                         | ==Transit Gateway== (TO DO)    | Central hub connecting many VPCs and on-prem networks                      |
|                         | Global Accelerator             | Sends users over the AWS backbone to the nearest healthy endpoint          |
|                         | PrivateLink                    | Private access to a service without crossing the internet                  |
| **Security & Identity** | IAM                            | Users, roles and policies deciding who can do what                         |
|                         | IAM Identity Center            | Single sign-on across accounts, federated with your directory              |
|                         | Cognito                        | Sign-up and sign-in for your application's end users                       |
|                         | KMS                            | Creates and controls encryption keys                                       |
|                         | CloudHSM                       | Dedicated hardware security modules you control                            |
|                         | Secrets Manager                | Stores and automatically rotates credentials                               |
|                         | ACM                            | Issues and renews TLS certificates                                         |
|                         | WAF                            | Filters malicious HTTP requests before they reach your app                 |
|                         | Shield                         | DDoS protection                                                            |
|                         | GuardDuty                      | Continuously detects threats from your logs                                |
|                         | Inspector                      | Scans workloads for known vulnerabilities                                  |
|                         | Macie                          | Finds sensitive data sitting in S3                                         |
|                         | Security Hub                   | Aggregates findings from the other security services                       |
| **Management**          | CloudWatch                     | Metrics, logs, alarms and dashboards                                       |
|                         | CloudTrail                     | Records every API call for audit                                           |
|                         | CloudFormation                 | Infrastructure as code from declarative templates                          |
|                         | Config                         | Records resource configuration and flags non-compliance                    |
|                         | Systems Manager                | Patching, remote access and automation across fleets                       |
|                         | Organizations                  | Manages many accounts under one billing and policy umbrella                |
|                         | Control Tower                  | Sets up a governed multi-account environment for you                       |
|                         | Trusted Advisor                | Recommendations on cost, security, limits and performance                  |
|                         | Service Catalog                | Approved templates that teams can deploy themselves                        |
| **Integration**         | SQS                            | Message queue that decouples producers from consumers                      |
|                         | SNS                            | Publish/subscribe notifications fanned out to many subscribers             |
|                         | EventBridge                    | Event bus that routes events to targets by rule                            |
|                         | Step Functions                 | Orchestrates multi-step workflows as a state machine                       |
|                         | AppSync                        | Managed GraphQL API layer                                                  |
|                         | Amazon MQ                      | Managed ActiveMQ/RabbitMQ for apps that already use them                   |
| **Analytics**           | Athena                         | SQL queries straight against data in S3, no servers                        |
|                         | Glue                           | Serverless ETL plus a central data catalog                                 |
|                         | EMR                            | Managed Spark and Hadoop clusters                                          |
|                         | Kinesis Data Streams           | Ingests real-time streaming data                                           |
|                         | Data Firehose                  | Delivers streams into S3, Redshift and others with no code                 |
|                         | MSK                            | Managed Apache Kafka                                                       |
|                         | OpenSearch                     | Search and log analytics                                                   |
|                         | QuickSight                     | Business intelligence dashboards                                           |
|                         | Lake Formation                 | Builds and secures a data lake                                             |
| **Migration**           | DMS                            | Migrates databases with minimal downtime                                   |
|                         | Application Migration Service  | Lift-and-shift of existing servers into EC2                                |
|                         | DataSync                       | Fast bulk file transfer to and from AWS                                    |
|                         | Transfer Family                | Managed SFTP/FTPS/FTP landing into S3                                      |
|                         | Migration Hub                  | Tracks migration progress across tools                                     |
| **Developer tools**     | CodeBuild                      | Compiles and tests code on managed build servers                           |
|                         | CodeDeploy                     | Rolls out releases to EC2, Lambda or ECS                                   |
|                         | CodePipeline                   | Chains build and deploy stages into a CI/CD pipeline                       |
|                         | X-Ray                          | Traces requests through a distributed application                          |
| **Cost**                | Cost Explorer                  | Visualises and forecasts your spend                                        |
|                         | Budgets                        | Alerts you when spend crosses a threshold                                  |
|                         | Compute Optimizer              | Recommends right-sized instances                                           |
| **AI / ML**             | SageMaker                      | Build, train and deploy machine learning models                            |
|                         | Bedrock                        | Access to foundation models through one API                                |
|                         | Rekognition                    | Image and video analysis                                                   |
|                         | Textract                       | Extracts text and data from documents                                      |
|                         | Comprehend                     | Natural language processing on text                                        |
|                         | Polly / Transcribe / Translate | Text-to-speech, speech-to-text, translation                                |

## In my own words


## Why it matters


## Links
- 
