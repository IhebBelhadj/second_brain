---
type: subtopic
created: 2026-10-10
topic: Infrastructure as code
tags: [subtopic, iac, gitops]
---
# GitOps

> What this covers: GitOps as an operating model for any target (Kubernetes, cloud infrastructure, VMs, application deploys): Git as the declared desired state, continuously reconciled by a controller next to the system. Then the Kubernetes version in depth (Argo CD, Flux): repository layout, promotion, drift and self-heal, rollback, secrets, many clusters.

Part of [[Infrastructure as code]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[GitOps basics]]: GitOps as an operating model, not a Kubernetes feature. From changes by hand, to files in Git applied by a pipeline (and why that alone isn't GitOps), to a controller that keeps reconciling: the three parts (Git repo, reconciliation controller, target), the replicas example, the four OpenGitOps principles. The same model on each target: Kubernetes (Argo CD, Flux), cloud infrastructure (Terraform/OpenTofu, which alone isn't a controller; scheduled plans, HCP Terraform, Crossplane/ACK), VMs (Ansible, Puppet, Chef agents, ansible-pull), application deploys. Push CI/CD vs GitOps table, CI builds the artifact and commits the version while the controller deploys, the three characteristics to check, and the traps (two owners for one value, disappearing hotfixes, unreviewed scheduled applies, "GitOps" with nothing reconciling)
- [[GitOps on Kubernetes]]: the Kubernetes version in depth. From `kubectl apply` on a laptop, to a pipeline that pushes with cluster credentials, to an agent in the cluster that pulls from Git and reconciles forever. App repo vs config repo, Kustomize base and overlays with images pinned by digest, CI that commits to Git instead of touching the cluster, promotion as a pull request, image automation, auto-sync vs self-heal vs report-only, pruning, one owner per field (HPA vs `replicas`), rollback as `git revert` (and why `kubectl rollout undo` gets overwritten), secrets (External Secrets, Sealed Secrets, SOPS), app of apps and ApplicationSet, rebuilding a cluster from Git, Argo CD vs Flux with both YAMLs, EKS, and the traps (endless OutOfSync, CRD ordering and sync waves, cascading Application deletes, reverted hotfixes, bad prunes, committed secrets, polling delays)

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
