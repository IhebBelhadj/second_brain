---
type: subtopic
created: 2026-10-09
topic: Containers
tags: [subtopic, containers]
---
# Containers › Kubernetes

> What this covers: Kubernetes itself: the model, the architecture, manifest syntax, a worked example and every object type.

Part of [[Containers]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[Kubernetes]]: the mental model first (a giant state machine: declaration → API → desired state → controllers watch → actual state → corrective action or wait, as chained loops), then what it adds over Swarm, object by object. Pods, Deployments and ReplicaSets, probes, requests and limits, Services and Ingress, ConfigMaps and Secrets, PVCs and StatefulSets, DaemonSets/Jobs/CronJobs, autoscaling, namespaces/RBAC/NetworkPolicies, CRDs and operators, Helm/Kustomize/GitOps, what it costs, and the classic failures (Pending, CrashLoopBackOff, liveness killing healthy apps, dropped requests on deploy, ImagePullBackOff)
- [[Kubernetes architecture]]: how it works under the hood, following one `kubectl apply`. etcd, the API server (authn, RBAC, admission, watch, optimistic concurrency), the controller manager, the scheduler, the kubelet with CRI/CNI/CSI and the pause container, EndpointSlices/kube-proxy/CoreDNS, the network model, every component's failure impact, and etcd latency, expired certificates, NotReady nodes, fighting controllers, webhooks
- [[Kubernetes manifest syntax]]: the grammar of every manifest. The four questions (apiVersion, kind, metadata, spec) plus status, the YAML underneath and when to quote, API groups and versions, names/labels/annotations and server-owned metadata, the repeating spec patterns (nested templates, label selectors, name references, named lists), the PodSpec field by field, units, the four ports, kinds without spec, conditions, `kubectl explain`/`--dry-run`, and the classic syntax failures
- [[Kubernetes worked example]]: a small e-commerce shop (frontend, backend, PostgreSQL) built object by object with full YAML: Namespace, ConfigMap, Secret, ServiceAccount, Role/RoleBinding, StatefulSet + PVC, Services, Deployments, Ingress with TLS, HPA, PodDisruptionBudget, NetworkPolicy, migration Job, CronJob, DaemonSet, StorageClass, the whole picture, the "one question per object" mental model, and the silent failures (label typos, missing keys, pending PVCs, stale config, Job names)
- Workloads: [[Kubernetes Pod]] (shared network and volumes, init and sidecar containers, phases, probes, QoS, shutdown) · [[Kubernetes ReplicaSet]] (keeping N pods, adoption, template hash) · [[Kubernetes Deployment]] (rolling updates, maxSurge/maxUnavailable, history and rollback, failed rollouts) · [[Kubernetes StatefulSet]] (ordinals, headless DNS, per-replica PVCs, ordered updates, partition, dead nodes) · [[Kubernetes DaemonSet]] (one pod per node, tolerations, node agents) · [[Kubernetes Job]] (completions, parallelism, retries, idempotence, indexed jobs) · [[Kubernetes CronJob]] (schedules, time zones, concurrency, missed runs)
- Networking: [[Kubernetes Service]] (ClusterIP/NodePort/LoadBalancer/ExternalName/headless, EndpointSlices, kube-proxy, traffic policies) · [[Kubernetes Ingress]] (controllers, classes, TLS, annotations, the Gateway API) · [[Kubernetes NetworkPolicy]] (label-based firewall, default deny, the AND/OR trap, CNI enforcement)
- Configuration: [[Kubernetes ConfigMap]] (env vs files, updates, hashed names) · [[Kubernetes Secret]] (types, what really protects it, keeping it out of Git, rotation)
- Storage: [[Kubernetes PersistentVolumeClaim]] (PV vs PVC, provisioning, access modes, reclaim, Multi-Attach, zones) · [[Kubernetes StorageClass]] (CSI drivers, reclaim policy, binding mode, defaults)
- Identity and access: [[Kubernetes ServiceAccount]] (bound tokens, OIDC workload identity) · [[Kubernetes RBAC]] (Role/ClusterRole/bindings, subjects, built-in roles, dangerous permissions)
- Cluster and tenancy: [[Kubernetes Namespace]] (scope, Pod Security admission, soft multi-tenancy) · [[Kubernetes Node]] (allocatable, conditions, affinity, taints and tolerations, drain, pressure eviction) · [[Kubernetes ResourceQuota and LimitRange]] (team budgets, defaults and bounds)
- Scaling and availability: [[Kubernetes HorizontalPodAutoscaler]] (the formula, metrics, behaviour, VPA/KEDA/cluster autoscaler) · [[Kubernetes PodDisruptionBudget]] (eviction API, what it does and doesn't cover, why the HPA's minReplicas doesn't replace it)
- Extending: [[Kubernetes CustomResourceDefinition]] (schemas, operators, versions, finalizers)

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
