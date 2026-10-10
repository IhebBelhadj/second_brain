---
type: concept
created: 2026-10-04
topic: Containers
subtopic: Kubernetes
confidence: 1
tags: [containers, kubernetes, kubernetes-object, security, secrets]
aliases: [Kubernetes Secrets, imagePullSecrets, External Secrets Operator, Sealed Secrets, Encryption at rest in Kubernetes]
---
# Kubernetes Secret

> [!abstract] In one sentence
> A Secret holds **sensitive data** (passwords, tokens, TLS keys, registry credentials) and is consumed like a [[Kubernetes ConfigMap]] (environment variables or files), but with a few protections: values are kept **out of pod specs**, volume files live **in memory** on the node, and access is controlled separately by RBAC (role-based access control). A Secret is **base64-encoded, not encrypted**: real protection comes from access control, **encryption at rest** in etcd, and keeping the values out of Git.

## Build-up: the database password

### Stage 1: where the password shouldn't be

The backend needs `DATABASE_PASSWORD`. It shouldn't be:
- in the **image** (anyone who can pull it can read it, see [[Docker]])
- in the **Deployment manifest** as plain `env` (it ends up in Git, in `kubectl get deployment -o yaml`, in every tool that reads Deployments)
- in a **ConfigMap** (readable by everyone allowed to read configuration)

It needs its own object, with its own permissions.

### Stage 2: the Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: database-secret
  namespace: shop
type: Opaque
stringData:                       # plain text in; stored base64-encoded under data:
  DATABASE_USER: shop_user
  DATABASE_PASSWORD: 4pP!x9-change-me
```

```bash
kubectl -n shop create secret generic database-secret \
  --from-literal=DATABASE_USER=shop_user --from-literal=DATABASE_PASSWORD='…'
kubectl -n shop get secret database-secret -o jsonpath='{.data.DATABASE_PASSWORD}' | base64 -d   # anyone allowed to read it can decode it
```

Consumed exactly like a ConfigMap:

```yaml
      envFrom:
        - secretRef: { name: database-secret }
      volumeMounts:
        - { name: tls, mountPath: /etc/tls, readOnly: true }
  volumes:
    - name: tls
      secret: { secretName: backend-tls, defaultMode: 0400 }
```

Built-in **types** validate the expected keys:

| Type | Holds | Used by |
|---|---|---|
| `Opaque` | Anything | Applications |
| `kubernetes.io/tls` | `tls.crt`, `tls.key` | [[Kubernetes Ingress]], Gateways, apps serving TLS (Transport Layer Security) |
| `kubernetes.io/dockerconfigjson` | Registry credentials | `imagePullSecrets` in pods or on a ServiceAccount, to pull private images |
| `kubernetes.io/basic-auth`, `kubernetes.io/ssh-auth` | Username/password, SSH (Secure Shell) key | Tools that expect those shapes |
| `kubernetes.io/service-account-token` | A long-lived ServiceAccount token | Legacy; avoid (see [[Kubernetes ServiceAccount]]) |

### Stage 3: what actually protects it

> [!warning] base64 is not encryption
> `c2hvcF91c2Vy` is `shop_user` to anyone. Encoding exists so binary data fits in YAML (YAML Ain't Markup Language), not to hide anything.

The real layers:

| Layer | Protects against | How |
|---|---|---|
| **RBAC** (role-based access control) | People and apps reading Secrets through the API (application programming interface) | Grant `get`/`list`/`watch` on `secrets` to as few subjects as possible ([[Kubernetes RBAC]]) |
| **Encryption at rest** | Someone reading etcd's data or backups | API server `EncryptionConfiguration`, ideally with a KMS (key management service) provider so the key lives outside the cluster. Off by default on self-managed clusters |
| **In-memory files** | Secrets left on node disks | Secret volumes are tmpfs on the node, only on nodes running a pod that uses them |
| **Kept out of Git** | Leaks through repositories | External secret managers or encrypted manifests (below) |

> [!warning] Who can create pods can read Secrets
> Anyone allowed to **create pods** in a namespace can mount any Secret of that namespace into a pod and print it, even without permission to read Secrets directly. Likewise, `list` on Secrets returns their **values**, not just names. Namespace boundaries and pod-creation rights are part of secret protection.

### Stage 4: keeping values out of Git

GitOps wants every manifest in Git; secrets can't be there in clear. The usual approaches:

| Approach | How | Trade-off |
|---|---|---|
| **External Secrets Operator** | An `ExternalSecret` object in Git says "sync `prod/db/password` from Vault / AWS (Amazon Web Services) Secrets Manager / GCP (Google Cloud Platform) Secret Manager into Secret `database-secret`" | The source of truth is the external manager, with its audit and rotation |
| **Sealed Secrets** | Values encrypted with a public key and committed; a controller in the cluster decrypts them into Secrets | Self-contained; the controller's private key becomes critical |
| **SOPS** (Secrets OPerationS) | Files encrypted in Git (keys in a KMS), decrypted by the deployment tool | Works with Helm/Kustomize/Argo CD plugins |
| **Secrets Store CSI (Container Storage Interface) driver** | Mounts secrets from an external manager directly as files, without (or alongside) a Secret object | Values never stored in etcd |

### Stage 5: rotation

A rotated database password must reach the pods. Files from a Secret volume update in place after a delay (not with `subPath`); environment variables don't change until a restart. Safe rotation means **both** values work for a while (the database accepts old and new), the Secret is updated, pods pick up the new value (restart or reload), then the old value is revoked.

## Advanced problems

### 1. The password appears in logs and crash reports
Environment variables are inherited by child processes and often dumped by error reporters and `/proc/<pid>/environ`. Files with restricted permissions leak less; prefer volumes for high-value secrets.

### 2. `ImagePullBackOff` on a private registry
The pod has no `imagePullSecrets` (or its ServiceAccount doesn't), or the Secret is in another namespace. Registry credentials are per namespace.

### 3. A Secret committed to Git
Deleting the commit isn't enough: the history, forks and clones keep it. Rotate the credential immediately, then clean up.

### 4. An etcd backup leaks everything
Without encryption at rest, an etcd snapshot contains every Secret in clear. Encrypt at rest and treat backups as secrets.

## Easy to get wrong
- Thinking base64 is encryption
- Committing Secret manifests with real values
- Granting `list` on secrets thinking it only shows names
- Forgetting that pod creation rights imply secret read rights in that namespace
- Encryption at rest left off on self-managed clusters
- Expecting env vars to pick up a rotated value
- Putting secrets in ConfigMaps or plain `env` values

## Related
- Non-sensitive counterpart:: [[Kubernetes ConfigMap]]
- Access control:: [[Kubernetes RBAC]], [[Kubernetes ServiceAccount]], [[Kubernetes Namespace]]
- TLS certificates:: [[Kubernetes Ingress]], [[Certificates and PKI]], [[TLS]]
- Concepts:: [[Encryption basics]], [[Workload identity (SPIFFE)]] (credentials without stored secrets)
- In AWS:: [[Systems Manager]] (Parameter Store), *[[Secrets Manager]]*
- Overview:: [[Kubernetes]], [[Kubernetes worked example]]
- Area:: [[Containers]]

## Flashcards
#flashcards

Is a Kubernetes Secret encrypted? :: No, only base64-encoded, unless encryption at rest is configured for etcd
What actually protects a Secret? :: RBAC, encryption at rest (ideally KMS), tmpfs volumes on nodes, keeping values out of Git
stringData vs data in a Secret? :: stringData takes plain text; data holds base64-encoded values
Secret type for TLS certificates? :: kubernetes.io/tls (tls.crt, tls.key)
Secret type for private registry credentials? :: kubernetes.io/dockerconfigjson, referenced by imagePullSecrets
Why can pod creators read Secrets? :: They can mount any Secret of the namespace into a pod
Does list on secrets return values? :: Yes, the full objects
Where are Secret volume files stored on the node? :: In memory (tmpfs)
How do teams keep Secrets out of Git? :: External Secrets Operator, Sealed Secrets, SOPS, or the Secrets Store CSI driver
Why prefer volumes over env vars for high-value secrets? :: Env vars leak to child processes, crash reports and /proc; files can be permission-restricted and update in place
