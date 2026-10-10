---
type: subtopic
created: 2026-10-09
topic: AWS
tags: [subtopic, aws]
---
# AWS compute

> What this covers: what runs my code: EC2, Auto Scaling, load balancers, Lambda, Lightsail, ECS, EKS, Packer.

Part of [[AWS]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[EC2]]: virtual machines, launch templates
- [[Load balancers]]: ALB / NLB and **target groups**
- [[Auto Scaling]]: grows and shrinks the number of EC2 instances
- [[Packer]]: golden AMIs from code. Bake vs fry, immutable infrastructure, how an `amazon-ebs` build works, a full template, cleaning the image (no secrets, host keys, cloud-init), building through Session Manager, encrypted AMIs shared across accounts and regions (the KMS trap), a CI pipeline with Parameter Store and instance refresh, vs EC2 Image Builder
- [[Lambda]]: run code without a server
- [[ECS]]: AWS's container orchestrator. Cluster, task definition, task, service, capacity providers, ECR with immutable tags, the two IAM roles, a service behind an ALB (`ip` targets), the endpoints private tasks need to pull images, rolling deploys with circuit breaker, scaling, Service Connect, ECS Exec, why tasks stop
- [[ECS tasks and task definitions]]: every field that matters, Fargate CPU/memory combinations, sidecars and `dependsOn`, how tasks get credentials, the task lifecycle, one-off/scheduled/orchestrated tasks (migrations, nightly jobs), stop codes and exit codes (137, 143)
- [[ECS on Fargate vs EC2]]: serverless tasks vs provisioning container instances myself (ECS-optimized AMI, ecs.config, Auto Scaling group + capacity provider with managed scaling and draining, placement strategies, bridge vs awsvpc, IMDS trap, daemon services, AMI refresh), cost, and when to choose which
- [[Kubernetes worked example on EKS]]: the Kubernetes shop moved to EKS with almost the same manifests. eksctl cluster (3-AZ VPC, managed node group, add-ons, Pod Identity), access entries, ECR, a Kustomize base + EKS overlay, StorageClass → EBS gp3, Ingress → ALB through the Load Balancer Controller (ACM, rule order), Secret from Secrets Manager via External Secrets, NetworkPolicies with the VPC CNI and the ALB, moving PostgreSQL to RDS, costs and the classic EKS failures
- [[ECS production stack]]: the whole thing from a GitHub repo, prod ready. Terraform state and GitHub OIDC roles (no keys), 3-AZ VPC with endpoints, Route 53 zone + ACM DNS-validated cert, HTTPS ALB + WAF, ECS on an EC2 Auto Scaling group with capacity provider, Secrets Manager injection and rotation, ECR + task definition + service, GitHub Actions build-once/promote with migrations and approvals, alarms, and the Fargate alternative
- [[Lightsail]]: the "easy mode" VPS
- [[EC2 vs Lightsail vs Lambda]]: which one should I pick?
- What is **VPC Lattice** exactly? (came up in [[Auto Scaling]])

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
