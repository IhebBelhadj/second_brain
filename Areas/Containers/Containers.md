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
- [[Docker Compose]]: from four `docker run` commands to one `compose.yaml`. Project names, the project network and service-name DNS, `depends_on` vs readiness (health checks), variables, override files and profiles, the `.env` trap, `compose watch`, running it on a server, and why it isn't an orchestrator (port conflicts when scaling, "lost" volumes, external networks, secrets)
- Not written yet: *[[Container internals]]* (namespaces, cgroups, overlay filesystems, OCI runtimes) · *[[Docker networking]]* (bridge, host, overlay networks, DNS between containers)

## 2. Orchestration
- [[Container orchestration]]: why a fleet of servers needs one. Declared desired state and the reconciliation loop (level-triggered), the jobs every orchestrator does, control plane vs workers, Raft quorum and odd manager counts, the products (Swarm, Kubernetes, Nomad, ECS), and quorum loss, manual fixes reverted, cascading reschedules, flapping health checks
- [[Docker Swarm]]: the orchestrator built into Docker Engine. `swarm init`/`join`, managers and Raft, services and tasks (replicated, global), the routing mesh, overlay networks and VIP discovery, stacks from Compose files (rolling updates, rollback, secrets, configs, placement), what it ignores and what it lacks, and its traps (quorum, VXLAN ports and MTU, address pool, pending tasks)
- [[Compose vs Swarm vs Kubernetes]]: one host vs a simple cluster vs an extensible platform, side by side, and when to pick each
- [[Deployment strategies]]: how traffic moves from v1 to v2. Deploy vs release, recreate, rolling (maxSurge/maxUnavailable, readiness), blue/green (the switch, cold green, draining, shared database), canary (traffic splitting, per-version metrics, low traffic), A/B testing vs canary, shadow traffic, feature flags, expand/contract migrations, a side-by-side table, and the traps (rollbacks that can't, no automatic rollback in Kubernetes, canaries that pass at 10%)

### Kubernetes
- [[Kubernetes]]: what it adds over Swarm, object by object. Pods, Deployments and ReplicaSets, probes, requests and limits, Services and Ingress, ConfigMaps and Secrets, PVCs and StatefulSets, DaemonSets/Jobs/CronJobs, autoscaling, namespaces/RBAC/NetworkPolicies, CRDs and operators, Helm/Kustomize/GitOps, what it costs, and the classic failures (Pending, CrashLoopBackOff, liveness killing healthy apps, dropped requests on deploy, ImagePullBackOff)
- [[Kubernetes architecture]]: how it works under the hood, following one `kubectl apply`. etcd, the API server (authn, RBAC, admission, watch, optimistic concurrency), the controller manager, the scheduler, the kubelet with CRI/CNI/CSI and the pause container, EndpointSlices/kube-proxy/CoreDNS, the network model, every component's failure impact, and etcd latency, expired certificates, NotReady nodes, fighting controllers, webhooks
- [[Kubernetes worked example]]: a small e-commerce shop (frontend, backend, PostgreSQL) built object by object with full YAML: Namespace, ConfigMap, Secret, ServiceAccount, Role/RoleBinding, StatefulSet + PVC, Services, Deployments, Ingress with TLS, HPA, PodDisruptionBudget, NetworkPolicy, migration Job, CronJob, DaemonSet, StorageClass, the whole picture, the "one question per object" mental model, and the silent failures (label typos, missing keys, pending PVCs, stale config, Job names)
- Objects, one note each (in reading order):
    - Workloads: [[Kubernetes Pod]] (shared network and volumes, init and sidecar containers, phases, probes, QoS, shutdown) · [[Kubernetes ReplicaSet]] (keeping N pods, adoption, template hash) · [[Kubernetes Deployment]] (rolling updates, maxSurge/maxUnavailable, history and rollback, failed rollouts) · [[Kubernetes StatefulSet]] (ordinals, headless DNS, per-replica PVCs, ordered updates, partition, dead nodes) · [[Kubernetes DaemonSet]] (one pod per node, tolerations, node agents) · [[Kubernetes Job]] (completions, parallelism, retries, idempotence, indexed jobs) · [[Kubernetes CronJob]] (schedules, time zones, concurrency, missed runs)
    - Networking: [[Kubernetes Service]] (ClusterIP/NodePort/LoadBalancer/ExternalName/headless, EndpointSlices, kube-proxy, traffic policies) · [[Kubernetes Ingress]] (controllers, classes, TLS, annotations, the Gateway API) · [[Kubernetes NetworkPolicy]] (label-based firewall, default deny, the AND/OR trap, CNI enforcement)
    - Configuration: [[Kubernetes ConfigMap]] (env vs files, updates, hashed names) · [[Kubernetes Secret]] (types, what really protects it, keeping it out of Git, rotation)
    - Storage: [[Kubernetes PersistentVolumeClaim]] (PV vs PVC, provisioning, access modes, reclaim, Multi-Attach, zones) · [[Kubernetes StorageClass]] (CSI drivers, reclaim policy, binding mode, defaults)
    - Identity and access: [[Kubernetes ServiceAccount]] (bound tokens, OIDC workload identity) · [[Kubernetes RBAC]] (Role/ClusterRole/bindings, subjects, built-in roles, dangerous permissions)
    - Cluster and tenancy: [[Kubernetes Namespace]] (scope, Pod Security admission, soft multi-tenancy) · [[Kubernetes Node]] (allocatable, conditions, affinity, taints and tolerations, drain, pressure eviction) · [[Kubernetes ResourceQuota and LimitRange]] (team budgets, defaults and bounds)
    - Scaling and availability: [[Kubernetes HorizontalPodAutoscaler]] (the formula, metrics, behaviour, VPA/KEDA/cluster autoscaler) · [[Kubernetes PodDisruptionBudget]] (eviction API, what it does and doesn't cover)
    - Extending: [[Kubernetes CustomResourceDefinition]] (schemas, operators, versions, finalizers)
- Not written yet: *[[Kubernetes networking]]* (CNI plugins, pod and Service ranges, Ingress and Gateway API in depth) · *[[Kubernetes storage]]* · *[[Helm]]*
- AWS: [[ECS]], [[ECS tasks and task definitions]], [[ECS on Fargate vs EC2]] (in the AWS area) · *[[EKS]]* (planned)

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
