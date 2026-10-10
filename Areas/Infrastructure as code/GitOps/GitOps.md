---
type: subtopic
created: 2026-10-10
topic: Infrastructure as code
tags: [subtopic, iac, gitops]
---
# GitOps

> What this covers: Git as the declared desired state, pulled and continuously reconciled by an agent next to the system (Argo CD, Flux on Kubernetes): push vs pull, repository layout, promotion, drift and self-heal, rollback, secrets, many clusters, and how far the idea goes outside Kubernetes.

Part of [[Infrastructure as code]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[GitOps basics]]: from `kubectl apply` on a laptop, to a pipeline that pushes with cluster credentials, to an agent in the cluster that pulls from Git and reconciles forever. The four OpenGitOps principles, app repo vs config repo, Kustomize base and overlays with images pinned by digest, CI that commits to Git instead of touching the cluster, promotion as a pull request, image automation, auto-sync vs self-heal vs report-only, pruning, one owner per field (HPA vs `replicas`), rollback as `git revert` (and why `kubectl rollout undo` gets overwritten), secrets (External Secrets, Sealed Secrets, SOPS), app of apps and ApplicationSet, rebuilding a cluster from Git, Argo CD vs Flux with both YAMLs, GitOps outside Kubernetes (Terraform in CI, Atlantis, Crossplane/ACK), and the traps (endless OutOfSync, CRD ordering and sync waves, cascading Application deletes, reverted hotfixes, bad prunes, committed secrets, polling delays)

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
