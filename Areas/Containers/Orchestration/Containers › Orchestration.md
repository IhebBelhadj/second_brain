---
type: subtopic
created: 2026-10-09
topic: Containers
tags: [subtopic, containers]
---
# Containers › Orchestration

> What this covers: running containers on many machines: orchestration concepts, Swarm, comparisons, deployment strategies, the Spring Cloud era.

Part of [[Containers]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[Container orchestration]]: why a fleet of servers needs one. Declared desired state and the reconciliation loop (level-triggered), the jobs every orchestrator does, control plane vs workers, Raft quorum and odd manager counts, the products (Swarm, Kubernetes, Nomad, ECS), and quorum loss, manual fixes reverted, cascading reschedules, flapping health checks
- [[Docker Swarm]]: the orchestrator built into Docker Engine. `swarm init`/`join`, managers and Raft, services and tasks (replicated, global), the routing mesh, overlay networks and VIP discovery, stacks from Compose files (rolling updates, rollback, secrets, configs, placement), what it ignores and what it lacks, and its traps (quorum, VXLAN ports and MTU, address pool, pending tasks)
- [[Compose vs Swarm vs Kubernetes]]: one host vs a simple cluster vs an extensible platform, side by side, and when to pick each
- [[Deployment strategies]]: how traffic moves from v1 to v2. Deploy vs release, recreate, rolling (maxSurge/maxUnavailable, readiness), blue/green (the switch, cold green, draining, shared database), canary (traffic splitting, per-version metrics, low traffic), A/B testing vs canary, shadow traffic, feature flags, expand/contract migrations, a side-by-side table, and the traps (rollbacks that can't, no automatic rollback in Kubernetes, canaries that pass at 10%)
- [[Spring Cloud and Netflix OSS]]: how microservices did discovery, balancing and resilience **inside the app** before orchestrators existed (Eureka, Ribbon, Feign, Hystrix, Zuul, Config Server, Sleuth/Zipkin), a full 2016 shop on EC2 VMs and how it was hosted on AWS (VPC tiers and security groups, baked AMIs, user data, Auto Scaling groups, how Eureka's own addresses were made stable, Config Server and the edge, red/black deploys with Asgard/Spinnaker, Beanstalk/ECS/Cloud Foundry alternatives), why it was right then and what hurt, and how each job moved into Kubernetes, the service mesh and AWS managed services (with the same shop rebuilt today, the migration path, and the traps: slow convergence, self-preservation, timeout and retry storms)

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
