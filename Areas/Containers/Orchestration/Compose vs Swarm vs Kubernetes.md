---
type: compare
created: 2026-10-04
topic: Containers
confidence: 1
tags: [containers, orchestration, compose, swarm, kubernetes]
---
# Compose vs Swarm vs Kubernetes

> [!abstract] The short answer
> **Compose** runs a multi-container application on **one host** (development, CI (continuous integration), small servers). **Swarm** runs the same Compose files on a **cluster** with failover, rolling updates and a routing mesh, and stays simple. **Kubernetes** is a cluster platform with a large, **extensible API (application programming interface)**: stateful workloads, autoscaling, access control, network policies, operators and a whole ecosystem, at the price of much more to learn and run.

## Side by side

| | [[Docker Compose]] | [[Docker Swarm]] | [[Kubernetes]] |
|---|---|---|---|
| Scope | One Docker host | A cluster of Docker hosts | A cluster of nodes with any CRI (Container Runtime Interface) runtime |
| Is it an orchestrator? | No | Yes | Yes |
| Install | A Docker CLI (command-line interface) plugin | Built into Docker Engine: `docker swarm init` | A distribution (kubeadm, k3s…) or a managed service |
| Description format | `compose.yaml` | `compose.yaml` + `deploy:` keys | Many YAML (YAML Ain't Markup Language) objects (often through Helm or Kustomize) |
| Unit scheduled | Container | Task (one container) | Pod (one or more containers sharing a network namespace) |
| State store | None (the Docker daemon) | Raft log inside the managers | etcd (Raft), behind the API server |
| Failure of a host | Everything down | Tasks rescheduled on other nodes | Pods rescheduled (after ~5 min by default) |
| Health checks | Recorded, used for `depends_on` | One health check: replace unhealthy tasks, gate updates | Separate startup, readiness and liveness probes |
| Rolling update / rollback | No (stop, then start) | Yes, with automatic rollback | Yes (ReplicaSets), with rollout history |
| Service discovery | DNS on the project network | DNS + virtual IP (Internet Protocol address) on overlay networks | Services (virtual IP + DNS), EndpointSlices |
| External traffic | Published ports on the host | Routing mesh on every node | NodePort, LoadBalancer, Ingress / Gateway API |
| Stateful services | Local volumes | Pinned by label; volume plugins rare | PVCs (PersistentVolumeClaims) + CSI (Container Storage Interface) drivers, StatefulSets, operators |
| Per-node agents, batch jobs | No | Global services; no jobs | DaemonSets, Jobs, CronJobs |
| Autoscaling | No | No | Pods (HPA, HorizontalPodAutoscaler) and nodes (Cluster Autoscaler, Karpenter) |
| Secrets | File mounts (`secrets:`) | Encrypted in Raft, mounted in memory | Secret objects (encryption at rest optional), external managers |
| Access control | Whoever has the Docker socket | Whoever reaches a manager (RBAC, role-based access control, only commercially) | RBAC per namespace and resource |
| Network isolation | Separate networks | Separate overlay networks | NetworkPolicies (with a CNI (Container Network Interface) plugin that enforces them) |
| Extensibility | None | None | CustomResourceDefinitions + controllers (operators) |
| Ecosystem | Development tooling | Small | Huge: Helm, Argo CD, cert-manager, Prometheus, service meshes, every cloud |
| Operating cost | Almost none | Low | High (control plane, upgrades every few months, add-ons) unless managed |

## What they share

- The same **images**: an OCI (Open Container Initiative) image built with `docker build` runs unchanged on all three
- The same **declarative** idea: describe what should run, let the tool converge to it. Compose does it once per `up`, Swarm and Kubernetes do it continuously
- Discovery **by name** through DNS (Domain Name System), and the same kernel building blocks underneath: namespaces, cgroups, veth pairs, bridges, NAT (network address translation)
- Compose is often used **alongside** the other two: on laptops and in CI for the same application that runs on Swarm or Kubernetes in production

## Where they actually differ

**Compose → Swarm** is a change of **scope**: one host becomes many. The file format barely changes, and the new things (managers, Raft, overlay networks, routing mesh, rolling updates) are what any [[Container orchestration]] needs. The learning cost is small.

**Swarm → Kubernetes** is a change of **model**. Swarm has a fixed set of objects designed for running stateless services. Kubernetes is an API where every concern is a separate object (pods, ReplicaSets, Services, Ingresses, PVCs, Roles, NetworkPolicies…), each handled by its own controller, and where new kinds of objects can be added. That makes it:
- **More capable**: stateful workloads, batch work, autoscaling, multi-team clusters with real isolation
- **More composable**: operators turn "run a PostgreSQL cluster" or "renew this certificate" into one object, and GitOps tools reconcile the cluster with a Git repository
- **More complex**: more moving parts (see [[Kubernetes architecture]]), more ways to fail, and add-ons (CNI, DNS, ingress, storage drivers) that are mine to choose and maintain

## If you have to choose

- One machine, development, CI, a small internal tool → **Compose**
- A few machines, stateless services, a small team that knows Compose, no cloud-managed option wanted → **Swarm**
- Many services or teams, stateful workloads, autoscaling, strict access control, or a need for the ecosystem (operators, GitOps, service mesh) → **Kubernetes**, preferably managed
- All-in on AWS (Amazon Web Services) and no need for Kubernetes' portability or ecosystem → also consider [[ECS]] (Elastic Container Service): an orchestrator with no control plane to run

## Flashcards
#flashcards

Compose vs Swarm, the main difference? :: Compose runs on one host. Swarm runs the same file format on a cluster with failover and rolling updates
Swarm vs Kubernetes, the main difference? :: Swarm has a fixed set of objects. Kubernetes is an extensible API with many object types, controllers and a large ecosystem
What does Kubernetes schedule vs Swarm? :: Pods (one or more containers) vs tasks (one container)
Which of Compose, Swarm, Kubernetes has autoscaling built in? :: Only Kubernetes (HPA; nodes via Cluster Autoscaler/Karpenter)
Which of the three supports custom object types? :: Only Kubernetes (CustomResourceDefinitions + controllers)
Where does each keep cluster state? :: Compose: none (Docker daemon). Swarm: Raft log in the managers. Kubernetes: etcd behind the API server
Do the three need different images? :: No, they all run the same OCI images
When is Swarm a reasonable choice? :: A few hosts, stateless services, a small team already using Compose
