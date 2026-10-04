# Area guide: Containers

**Index:** `Containers.md` is the learning path with a one-line summary of every note and the planned notes as italic links. Read it for *what* a note covers; use this file for *where* it is.

**Scope:** vendor-neutral containers for a systems engineer: building, tagging and shipping images, running containers, container internals, orchestration concepts. AWS container services (ECS, Fargate, ECR) live in `Areas/AWS/Compute/` with `topic: AWS` and are linked from section 2 of the index.

## Folder map

```
Containers/
├── Containers.md                  topic index (the learning path)
├── Docker.md                      images/layers/cache, Dockerfile order, secrets, multi-stage, PID 1, ports, volumes, deploy flow, multi-arch, traps
├── Docker image tags.md           tags vs digests, latest, moving tags, immutability, deploy by digest, promotion, base pinning, multi-arch, retention
├── Docker Compose.md              compose.yaml, project network/DNS, depends_on + healthchecks, overrides/profiles/.env, watch, single-host limits
├── Orchestration/                 vendor-neutral orchestration concepts and Swarm
│   ├── Container orchestration.md desired state, reconciliation loop, jobs of an orchestrator, control plane/workers, Raft quorum, products
│   ├── Docker Swarm.md            managers/workers, services/tasks, routing mesh, overlay networks, stacks, rolling updates, secrets, limits
│   ├── Compose vs Swarm vs Kubernetes.md   compare: scope, features, ecosystem, when to choose each
│   └── Deployment strategies.md   recreate, rolling, blue/green, canary, A/B, shadow, feature flags, expand/contract
└── Kubernetes/                    Kubernetes itself (vendor-neutral; EKS goes in the AWS area)
    ├── Kubernetes.md              the objects: pods, Deployments, probes, Services/Ingress, config, storage/StatefulSets, autoscaling, RBAC, CRDs/operators
    └── Kubernetes architecture.md components under the hood: etcd, API server, controllers, scheduler, kubelet/CRI/CNI/CSI, kube-proxy, CoreDNS
```

`ECS.md`, `ECS tasks and task definitions.md` and `ECS on Fargate vs EC2.md` are listed in this area's index (section 2) but live in `Areas/AWS/Compute/` with `topic: AWS`.

## Where a new note goes

| It's about… | Folder |
|---|---|
| Images, Dockerfiles, registries, running containers (section 1) | Area root |
| Internals: namespaces, cgroups, runtimes | Area root |
| Orchestration concepts, Swarm, comparisons (section 2) | `Orchestration/` |
| Kubernetes, vendor-neutral (section 2, "Kubernetes") | `Kubernetes/` |
| An AWS container service (ECS, EKS, App Runner, ECR) | `Areas/AWS/Compute/`, `topic: AWS`, listed in section 2 of `Containers.md` |

The planned notes (roadmap) are the italic `*[[…]]*` links in `Containers.md`: when writing one, use that exact name so existing links resolve.
