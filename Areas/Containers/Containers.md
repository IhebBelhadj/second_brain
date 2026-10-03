---
type: topic
created: 2026-10-03
tags: [topic]
---
# Containers

> What this covers: packaging and running applications as **containers**: how images are built, named and shipped, how containers run on a host, and how orchestrators run many of them. Vendor-neutral first. AWS (ECS, Fargate, ECR) is one place it's applied, and lives in the AWS area.

## How to use this

Read top to bottom. Links in *italics* are notes not written yet (the roadmap).

## 1. Images and containers
- [[Docker]]: from "it works on my machine" to an image. Layers and the build cache, instruction order, secrets that stay in layers, multi-stage builds, BuildKit cache and secret mounts, PID 1 and signals, ports and bind addresses, volumes, the build-once deployment flow, multi-arch builds, and the production traps (published ports bypassing the firewall, Docker Hub limits behind NAT, full disks, exit 137)
- [[Docker image tags]]: learning tags hands-on (untagged images, `-t`, several tags on one image, rebuilding moves a tag, full names with the registry, pushing, digests vs tags, pulling on other machines), choosing a tagging scheme (commit, release, floating, environment tags), build once and promote, deploying by digest, and what goes wrong (`latest`, races, moving base images, fake rollbacks, multi-arch, retention)
- Not written yet: *[[Container internals]]* (namespaces, cgroups, overlay filesystems, OCI runtimes) · *[[Docker networking]]* (bridge, host, overlay networks, DNS between containers) · *[[Docker Compose]]*

## 2. Orchestration
- AWS: [[ECS]], [[ECS tasks and task definitions]], [[ECS on Fargate vs EC2]] (in the AWS area)
- Not written yet: *[[Kubernetes]]*

## Related areas
- [[Networking]]: namespaces and veth pairs ([[Network interfaces]]), published ports as DNAT ([[NAT and PAT]]), [[Sockets]], [[Inter-process communication]]
- [[AWS]]: ECR, ECS, Fargate, and [[Packer]] for machine images

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE topic = this.file.name AND confidence
SORT confidence ASC
```

## Open questions
- 
