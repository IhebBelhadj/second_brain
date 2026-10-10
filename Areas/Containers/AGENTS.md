# Area guide: Containers

**Index:** `Containers.md` is the learning path with a one-line summary of every note and the planned notes as italic links. Read it for *what* a note covers; use this file for *where* it is.

**Scope:** vendor-neutral containers for a systems engineer: building, tagging and shipping images, running containers, container internals, orchestration concepts. AWS container services (ECS, Fargate, ECR) live in `Areas/AWS/Compute/` with `topic: AWS` and are linked from section 2 of the index.

## Folder map

```
Containers/
├── Containers.md                  topic index (the learning path)
├── Docker basics.md               images/layers/cache, Dockerfile order, secrets, multi-stage, PID 1, ports, volumes, deploy flow, multi-arch, traps
├── Docker image tags.md           tags vs digests, latest, moving tags, immutability, deploy by digest, promotion, base pinning, multi-arch, retention
├── Docker Compose.md              compose.yaml, project network/DNS, depends_on + healthchecks, overrides/profiles/.env, watch, single-host limits
├── Orchestration/                 vendor-neutral orchestration concepts and Swarm
│   ├── Container orchestration basics.md desired state, reconciliation loop, jobs of an orchestrator, control plane/workers, Raft quorum, products
│   ├── Docker Swarm.md            managers/workers, services/tasks, routing mesh, overlay networks, stacks, rolling updates, secrets, limits
│   ├── Compose vs Swarm vs Kubernetes.md   compare: scope, features, ecosystem, when to choose each
│   ├── Deployment strategies.md   recreate, rolling, blue/green, canary, A/B, shadow, feature flags, expand/contract
│   └── Spring Cloud and Netflix OSS.md   Eureka/Ribbon/Hystrix/Zuul/Config era, 2016 VM architecture, what replaced each piece (Kubernetes, mesh, AWS)
└── Kubernetes/                    Kubernetes itself (vendor-neutral; EKS goes in the AWS area)
    ├── Kubernetes basics.md       the objects: pods, Deployments, probes, Services/Ingress, config, storage/StatefulSets, autoscaling, RBAC, CRDs/operators
    ├── Kubernetes architecture.md components under the hood: etcd, API server, controllers, scheduler, kubelet/CRI/CNI/CSI, kube-proxy, CoreDNS
    ├── Kubernetes manifest syntax.md   apiVersion/kind/metadata/spec/status, YAML types, API groups, labels/selectors, PodSpec, units, ports, kubectl explain
    ├── Kubernetes worked example.md   e-commerce shop with every common object in YAML, step by step, and the mental model
    └── Objects/                   one note per object type, all named "Kubernetes <Kind>"
        ├── Kubernetes Pod.md, Kubernetes ReplicaSet.md, Kubernetes Deployment.md, Kubernetes StatefulSet.md,
        │   Kubernetes DaemonSet.md, Kubernetes Job.md, Kubernetes CronJob.md                     workloads
        ├── Kubernetes Service.md, Kubernetes Ingress.md (+ Gateway API), Kubernetes NetworkPolicy.md   networking
        ├── Kubernetes ConfigMap.md, Kubernetes Secret.md                                          configuration
        ├── Kubernetes PersistentVolumeClaim.md (+ PV), Kubernetes StorageClass.md                 storage
        ├── Kubernetes ServiceAccount.md, Kubernetes RBAC.md (Role, ClusterRole, bindings)         identity and access
        ├── Kubernetes Namespace.md, Kubernetes Node.md, Kubernetes ResourceQuota and LimitRange.md   cluster and tenancy
        ├── Kubernetes HorizontalPodAutoscaler.md, Kubernetes PodDisruptionBudget.md              scaling and availability
        └── Kubernetes CustomResourceDefinition.md                                                 extending (operators)
```

`ECS.md`, `ECS tasks and task definitions.md` and `ECS on Fargate vs EC2.md` are listed in this area's index (section 2) but live in `Areas/AWS/Compute/` with `topic: AWS`.

## Sub-topics

Every note in this area has `subtopic: <index name>` in its frontmatter, and is linked from that sub-topic index (`type: subtopic`, tag `subtopic`). The area index `Containers.md` links every sub-topic index in its "Sub-topics" section.

| Sub-topic index | Lives in | Covers |
|---|---|---|
| `Docker.md` | `(area root)` | building, tagging and running images on one host: Docker, tags, Compose |
| `Container orchestration.md` | `Orchestration/` | running containers on many machines: orchestration concepts, Swarm, comparisons, deployment strategies, the Spring Cloud era |
| `Kubernetes.md` | `Kubernetes/` | Kubernetes itself: the model, the architecture, manifest syntax, a worked example and every object type |

A new note gets the `subtopic` of the folder it goes in (notes at the area root: see the table), and a line in that sub-topic index as well as in `Containers.md`.

## Where a new note goes

| It's about… | Folder |
|---|---|
| Images, Dockerfiles, registries, running containers (section 1) | Area root |
| Internals: namespaces, cgroups, runtimes | Area root |
| Orchestration concepts, Swarm, comparisons (section 2) | `Orchestration/` |
| Kubernetes, vendor-neutral (section 2, "Kubernetes") | `Kubernetes/`; a note about one object type goes in `Kubernetes/Objects/`, named `Kubernetes <Kind>` |
| An AWS container service (ECS, EKS, App Runner, ECR) | `Areas/AWS/Compute/`, `topic: AWS`, listed in section 2 of `Containers.md` |

The planned notes (roadmap) are the italic `*[[…]]*` links in `Containers.md`: when writing one, use that exact name so existing links resolve.
