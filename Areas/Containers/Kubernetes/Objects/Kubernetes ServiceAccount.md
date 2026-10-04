---
type: concept
created: 2026-10-04
topic: Containers
confidence: 1
tags: [containers, kubernetes, kubernetes-object, identity, security]
aliases: [ServiceAccount, ServiceAccounts, Service account token, Bound service account token, Projected service account token]
---
# Kubernetes ServiceAccount

> [!abstract] In one sentence
> A ServiceAccount is the **identity a pod runs as**: a namespaced object (`system:serviceaccount:shop:backend`) for which the kubelet mounts a **short-lived, audience-bound, automatically rotated token** into the pod. The token authenticates the pod to the Kubernetes API (where [[Kubernetes RBAC]] decides what it may do) and, because the cluster acts as an **OIDC issuer**, to outside systems such as cloud IAM, Vault or other clusters, without any stored secret.

## Build-up: a pod that needs an identity

### Stage 1: who is calling?

Some pods talk to the Kubernetes API: an ingress controller watches Ingress objects, a CI (continuous integration) runner creates pods, the backend reloads a ConfigMap. The API server must know **who** each caller is to apply permissions. Humans have certificates or OIDC (OpenID Connect) logins; pods need their own identity, and it must not be a password copied into an image.

Kubernetes has no "User" objects at all: people are authenticated by external means. **ServiceAccounts are the only identities Kubernetes stores itself**, and they're meant for workloads.

### Stage 2: the object and how a pod uses it

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: backend
  namespace: shop
automountServiceAccountToken: true     # default; set false on accounts whose pods never call the API
---
# pod template:
spec:
  serviceAccountName: backend
```

Every namespace gets a ServiceAccount named `default` automatically, and pods that don't name one run as it. Giving each workload **its own** account keeps permissions separate: what's granted to `default` is granted to every pod that forgot to choose.

What the pod receives:

```
/var/run/secrets/kubernetes.io/serviceaccount/
├── token        ← a JWT, valid ~1 hour, rotated by the kubelet before it expires
├── ca.crt       ← the cluster CA, to verify the API server's certificate
└── namespace    ← "shop"
```

The token is a JWT (JSON Web Token, see [[JWT and bearer tokens]]), signed by the API server, with claims like:

```json
{
  "iss": "https://kubernetes.default.svc",
  "sub": "system:serviceaccount:shop:backend",
  "aud": ["https://kubernetes.default.svc"],
  "exp": 1791234567,
  "kubernetes.io": { "namespace": "shop", "pod": { "name": "backend-5b8e21-x7k2p" }, "serviceaccount": { "name": "backend" } }
}
```

It's **bound**: to an audience, to an expiry, and to the pod's lifetime. When the pod is deleted, the token stops being valid even before it expires. Client libraries (client-go and others) read it automatically when running in a cluster. CA means certificate authority; JSON is JavaScript Object Notation.

> [!info] The old long-lived tokens
> Before Kubernetes 1.24, each ServiceAccount got a Secret holding a **token that never expired**, and anyone who read that Secret had the account's permissions forever. Those Secrets are no longer created automatically. If a long-lived token is really needed (an external system that can't refresh), it can still be created explicitly, but `kubectl create token backend --duration=1h` (short-lived) is the normal way to get one by hand.

### Stage 3: permissions

A ServiceAccount has **no permissions** by itself (beyond basic discovery). A RoleBinding grants them:

```bash
kubectl -n shop create rolebinding backend-reads-config \
  --role=backend-config-reader --serviceaccount=shop:backend
kubectl auth can-i list configmaps -n shop --as=system:serviceaccount:shop:backend    # yes
kubectl auth can-i list secrets -n shop --as=system:serviceaccount:shop:backend       # no
```

Each account is also in the groups `system:serviceaccounts` (all of them) and `system:serviceaccounts:shop` (all in the namespace), which bindings can target.

### Stage 4: identity outside the cluster (workload identity)

The cluster publishes its token-signing public keys at an OIDC discovery endpoint. So the same mechanism works **outside** Kubernetes: a pod requests a token with another **audience** (projected volume), and an external system that trusts the cluster as an OIDC issuer verifies it:

```yaml
  volumes:
    - name: vault-token
      projected:
        sources:
          - serviceAccountToken:
              audience: vault.example.com
              expirationSeconds: 3600
              path: token
```

- **Cloud IAM** (identity and access management): AWS (Amazon Web Services) IRSA (IAM Roles for Service Accounts) and EKS (Elastic Kubernetes Service) Pod Identity, GCP (Google Cloud Platform) Workload Identity and Azure Workload Identity exchange the pod's token for cloud credentials. No cloud keys in Secrets
- **Vault** and other secret managers authenticate pods the same way
- A [[Service mesh]] issues each workload a certificate whose identity is its ServiceAccount (`spiffe://cluster.local/ns/shop/sa/backend`, see [[Workload identity (SPIFFE)]])

This is the general idea from [[OpenID Connect]]: short-lived tokens from an issuer the receiver already trusts, instead of shared secrets.

## Advanced problems

### 1. A compromised pod with too many rights
A pod's token can be read by anyone who gets code execution in it. If its ServiceAccount (often `default`, with permissions someone granted for convenience) can list Secrets or create pods, the attacker inherits that. One account per workload, minimal permissions, and `automountServiceAccountToken: false` for pods that never call the API.

### 2. `403 Forbidden` from the API
`User "system:serviceaccount:shop:backend" cannot list resource "configmaps"`: the account authenticated fine, but no binding grants the verb. `kubectl auth can-i --as=…` reproduces it; check the binding's namespace and the Role's `apiGroups`.

### 3. An external system rejects the token
The audience doesn't match what the system expects, the token expired because the app read it once at startup and cached it (it must re-read the file), or the system doesn't trust the cluster's issuer URL (uniform resource locator).

## Easy to get wrong
- Running every pod as the `default` ServiceAccount and granting it permissions
- Thinking Kubernetes has User objects: only ServiceAccounts are stored
- Expecting ServiceAccount tokens to last forever: projected tokens expire and rotate
- Caching the token at startup instead of re-reading the file
- Mounting tokens into pods that never call the API
- Using long-lived token Secrets for external systems that could use OIDC federation

## Related
- Permissions:: [[Kubernetes RBAC]]
- Used by:: [[Kubernetes Pod]]
- Token format and trust:: [[JWT and bearer tokens]], [[OpenID Connect]], [[Workload identity (SPIFFE)]], [[Service mesh]]
- Registry credentials:: [[Kubernetes Secret]] (imagePullSecrets can be set on the ServiceAccount)
- Overview:: [[Kubernetes]], [[Kubernetes architecture]] (authentication), [[Kubernetes worked example]]
- Area:: [[Containers]]

## Flashcards
#flashcards

What is a ServiceAccount? :: A namespaced identity for pods, used to authenticate to the Kubernetes API and, via OIDC, to external systems
Full name of ServiceAccount backend in namespace shop? :: system:serviceaccount:shop:backend
What ServiceAccount does a pod use if none is set? :: The namespace's default ServiceAccount
What does the kubelet mount for a ServiceAccount? :: A short-lived bound token (JWT), the cluster CA certificate, and the namespace
How long do projected ServiceAccount tokens live? :: About an hour by default, rotated automatically, and invalid once the pod is deleted
Are long-lived ServiceAccount token Secrets created automatically? :: No, not since Kubernetes 1.24
Does a ServiceAccount have permissions by itself? :: No, RoleBindings or ClusterRoleBindings grant them
How do you test a ServiceAccount's permissions? :: kubectl auth can-i <verb> <resource> --as=system:serviceaccount:<ns>:<name>
How do pods get cloud credentials without stored keys? :: Their ServiceAccount token (OIDC) is exchanged for cloud credentials (IRSA, Pod Identity, Workload Identity)
What does automountServiceAccountToken: false do? :: Stops mounting the API token into pods that don't need it
Does Kubernetes have User objects? :: No. Users are authenticated externally; only ServiceAccounts are stored
