---
type: concept
created: 2026-10-04
topic: Containers
subtopic: Kubernetes
confidence: 1
tags: [containers, kubernetes, kubernetes-object, scheduling, nodes]
aliases: [Kubernetes nodes, Taints and tolerations, Taint, Toleration, kubectl drain, Node affinity, Allocatable]
---
# Kubernetes Node

> [!abstract] In one sentence
> A Node object represents **one machine that runs pods**, registered by its kubelet: it reports **capacity and allocatable** resources, **conditions** (Ready, MemoryPressure, DiskPressure…) and a heartbeat, and carries the **labels** and **taints** that the scheduler uses to decide which pods may land there. Nodes are also what operators **cordon, drain and replace** during maintenance.

## Build-up: placing the shop's pods on the right machines

### Stage 1: a node registers itself

When the kubelet starts on a machine, it creates (or updates) a Node object named after the host:

```bash
kubectl get nodes -o wide
kubectl describe node node-2
```

```
Name:      node-2
Labels:    kubernetes.io/hostname=node-2
           kubernetes.io/arch=amd64
           topology.kubernetes.io/zone=zone-b
           node.kubernetes.io/instance-type=standard-8
Taints:    <none>
Conditions:
  Ready            True     kubelet is posting ready status
  MemoryPressure   False
  DiskPressure     False
  PIDPressure      False
Capacity:     cpu: 8      memory: 32Gi    pods: 110
Allocatable:  cpu: 7800m  memory: 30.5Gi  pods: 110
Allocated resources (requests): cpu 6100m (78%)  memory 22Gi (72%)
```

- **Capacity** is the machine; **allocatable** is what's left for pods after reserving resources for the OS (operating system), the kubelet and the container runtime (`system-reserved`, `kube-reserved`) and the eviction threshold. The scheduler fits pods' **requests** into allocatable
- **Conditions** are the kubelet's health report. The heartbeat is a Lease object in `kube-node-lease`, renewed every 10 seconds; when it stops, the node lifecycle controller marks the node `NotReady` ([[Kubernetes architecture]])
- **Labels** describe the machine: zone, architecture, instance type, plus any custom labels (`disk=ssd`, `pool=gpu`)

### Stage 2: attracting pods to nodes

The search service needs SSD (solid-state drive) nodes; the shop's replicas should spread across zones.

```yaml
spec:
  nodeSelector:                       # simplest: must have these labels
    disk: ssd
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:      # hard rule
        nodeSelectorTerms:
          - matchExpressions:
              - { key: kubernetes.io/arch, operator: In, values: [amd64, arm64] }
      preferredDuringSchedulingIgnoredDuringExecution:     # soft preference
        - weight: 50
          preference:
            matchExpressions:
              - { key: topology.kubernetes.io/zone, operator: In, values: [zone-a] }
  topologySpreadConstraints:          # spread replicas evenly across zones
    - maxSkew: 1
      topologyKey: topology.kubernetes.io/zone
      whenUnsatisfiable: DoNotSchedule
      labelSelector: { matchLabels: { app: backend } }
```

"IgnoredDuringExecution" means the rule is checked **at scheduling** only: relabelling a node later doesn't move running pods. (Pod affinity and anti-affinity do the same relative to **other pods**: "not on a node that already runs a backend pod".)

### Stage 3: repelling pods with taints

The GPU (graphics processing unit) nodes are expensive and must run **only** GPU workloads. Affinity attracts the GPU pods, but nothing stops other pods from landing there. A **taint** does: it repels every pod that doesn't explicitly **tolerate** it.

```bash
kubectl taint nodes gpu-1 dedicated=gpu:NoSchedule
```

```yaml
# only pods with this toleration may be scheduled on gpu-1
spec:
  tolerations:
    - { key: dedicated, operator: Equal, value: gpu, effect: NoSchedule }
  nodeSelector: { pool: gpu }        # and this makes them go there (a toleration only permits)
```

| Effect | New pods without toleration | Running pods without toleration |
|---|---|---|
| `PreferNoSchedule` | Avoided if possible | Stay |
| `NoSchedule` | Not scheduled | Stay |
| `NoExecute` | Not scheduled | **Evicted** (after `tolerationSeconds` if set) |

Kubernetes itself uses taints: control plane nodes carry `node-role.kubernetes.io/control-plane:NoSchedule`; a node that stops reporting gets `node.kubernetes.io/unreachable:NoExecute`, and pods tolerate it for **300 seconds** by default, which is why pods of a dead node are replaced after about 5 minutes.

> [!info] Taint + label for dedicated nodes
> A taint keeps others **out**; a node selector or affinity brings the right pods **in**. Dedicated node pools need both.

### Stage 4: maintenance

```bash
kubectl cordon node-2          # unschedulable: no new pods, running ones stay
kubectl drain node-2 --ignore-daemonsets --delete-emptydir-data   # evict pods (respecting PDBs), then cordon
# … patch, reboot, upgrade …
kubectl uncordon node-2        # schedulable again
kubectl delete node node-2     # if the machine is gone for good
```

`drain` uses the **eviction API (application programming interface)**, which respects [[Kubernetes PodDisruptionBudget|PodDisruptionBudgets]]: it waits when evicting a pod would leave too few replicas. DaemonSet pods are skipped (they'd come straight back), and pods with `emptyDir` data need the explicit flag because that data is lost.

### Stage 5: node-pressure eviction

When a node runs low on memory or disk, the **kubelet** evicts pods itself to protect the node (default hard threshold: `memory.available < 100Mi`). It picks pods by QoS (quality of service) class and usage relative to requests: BestEffort first, then Burstable pods using more than they requested ([[Kubernetes Pod]]). This eviction **doesn't** respect PodDisruptionBudgets: it's an emergency, not maintenance. Setting realistic memory requests is the protection.

## Advanced problems

### 1. Node `NotReady`
The kubelet stopped reporting: the machine is down, the kubelet or container runtime crashed, the node can't reach the API server, or a full disk or exhausted PIDs (process IDs) froze it. `kubectl describe node` shows the last conditions; then the machine's kubelet logs (`journalctl -u kubelet`).

### 2. Pods `Pending` with `untolerated taint`
The only nodes with room are tainted. Either the pod needs the toleration, or the taint is leftover (`node.kubernetes.io/unschedulable` from a forgotten cordon, `disk-pressure` from a full disk).

### 3. A drain hangs
A PodDisruptionBudget can't be satisfied (single replica with `minAvailable: 1`), or a pod without a controller (a bare pod) blocks it (`--force` deletes it for good). Fix the PDB (PodDisruptionBudget) rather than forcing.

### 4. Allocatable looks fine, but the node is overloaded
Requests are reservations, not usage. Pods with low requests and high real usage (or no limits) overcommit the node, causing throttling and node-pressure evictions. Requests must reflect real usage.

## Easy to get wrong
- Thinking a toleration attracts a pod to a node: it only permits; use a selector or affinity too
- Expecting affinity changes to move running pods ("IgnoredDuringExecution")
- Confusing capacity with allocatable
- Expecting node-pressure evictions to respect PDBs
- Draining without PDBs: all replicas of a service evicted at once
- Forgetting to uncordon after maintenance

## Related
- Runs:: [[Kubernetes Pod]], [[Kubernetes DaemonSet]]
- Maintenance protection:: [[Kubernetes PodDisruptionBudget]]
- Agent and heartbeats:: [[Kubernetes architecture]] (kubelet, node lifecycle controller)
- Scope:: [[Kubernetes Namespace]] (nodes are cluster-scoped)
- Overview:: [[Kubernetes]]
- In AWS (Amazon Web Services):: [[EC2]], [[Auto Scaling]] (node groups)
- Area:: [[Containers]]

## Flashcards
#flashcards

What creates a Node object? :: The kubelet registers its machine
Capacity vs allocatable? :: Capacity is the machine. Allocatable is what's left for pods after system/kube reservations and eviction thresholds
Main node conditions? :: Ready, MemoryPressure, DiskPressure, PIDPressure
How do nodes send heartbeats? :: Lease objects in kube-node-lease, renewed every 10 s
nodeSelector vs node affinity? :: nodeSelector: required exact labels. Affinity: required or preferred rules with operators
What does IgnoredDuringExecution mean? :: The rule only applies at scheduling; running pods aren't moved
What does a taint do? :: Repels pods that don't tolerate it
Taint effects? :: PreferNoSchedule, NoSchedule, NoExecute (also evicts running pods)
Does a toleration make a pod go to a tainted node? :: No, it only permits it; add a selector or affinity
How long do pods tolerate an unreachable node by default? :: 300 seconds
cordon vs drain? :: cordon stops new pods. drain evicts pods (respecting PDBs) and cordons
Does kubelet node-pressure eviction respect PDBs? :: No
