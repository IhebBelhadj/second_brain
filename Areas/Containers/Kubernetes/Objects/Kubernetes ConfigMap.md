---
type: concept
created: 2026-10-04
topic: Containers
subtopic: Containers › Kubernetes
confidence: 1
tags: [containers, kubernetes, kubernetes-object, configuration]
aliases: [ConfigMap, ConfigMaps, envFrom]
---
# Kubernetes ConfigMap

> [!abstract] In one sentence
> A ConfigMap holds **non-sensitive configuration** as key-value pairs or whole files, separate from the image, so **the same image runs in every environment** with different settings. Pods consume it as **environment variables** (read once, at container start) or as **files in a mounted volume** (updated in place after a delay); changing a ConfigMap doesn't restart anything by itself.

## Build-up: one image, three environments

### Stage 1: configuration in the image

The backend image contains `config.yaml` with `log_level: debug` and the database host of the staging environment. Production needs other values, so the team builds a second image. Now staging and production run **different builds**, and what was tested isn't what's deployed (the problem [[Docker image tags]] warns about: build once, promote the same image).

Configuration that varies by environment must come from **outside** the image, at run time.

### Stage 2: the ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: backend-config
  namespace: shop
data:
  LOG_LEVEL: "info"                 # values are always strings
  DATABASE_HOST: "postgres"
  FEATURE_NEW_CHECKOUT: "false"
  app.yaml: |                       # a whole file as one key
    cache:
      ttl_seconds: 300
    payments:
      provider_url: https://payments.example.com
```

```bash
# the same object from files and literals:
kubectl -n shop create configmap backend-config \
  --from-file=app.yaml --from-literal=LOG_LEVEL=info --dry-run=client -o yaml
```

Limit: **1 MiB** per ConfigMap (it's stored in etcd). It's meant for configuration, not data. `binaryData` holds base64-encoded binary values.

### Stage 3: consuming it

```yaml
spec:
  containers:
    - name: backend
      image: registry.example.com/shop-backend:1.5.0
      envFrom:                                   # every key → an environment variable
        - configMapRef: { name: backend-config }
      env:
        - name: LOG_LEVEL                        # or one key, possibly renamed
          valueFrom:
            configMapKeyRef: { name: backend-config, key: LOG_LEVEL }
      volumeMounts:
        - { name: config, mountPath: /etc/shop, readOnly: true }
  volumes:
    - name: config
      configMap:
        name: backend-config
        items:
          - { key: app.yaml, path: app.yaml }    # → /etc/shop/app.yaml
```

| Way | Updated when the ConfigMap changes? | Good for |
|---|---|---|
| **Environment variables** (`env`, `envFrom`) | **No**, until the container restarts | Simple settings read at startup |
| **Volume** (files) | **Yes**, after a delay (up to about a minute, the kubelet's sync plus cache) | Config files, apps that watch and reload them |
| Volume with `subPath` | **No** | Mounting a single file into an existing directory (at the cost of updates) |
| Read through the Kubernetes API (application programming interface) | Immediately (with a watch) | Apps that reload dynamically; needs RBAC ([[Kubernetes RBAC]]) |

`envFrom` skips keys that aren't valid variable names (like `app.yaml`); `prefix: CFG_` adds a prefix to all names.

### Stage 4: rolling out a configuration change

Changing `LOG_LEVEL` in the ConfigMap changes nothing in running pods that read it as an environment variable. Options:
- `kubectl rollout restart deployment/backend`: new pods read the new values
- **Hash in the name**: Kustomize's `configMapGenerator` (and Helm patterns) create `backend-config-7f2k9c` with a content hash in the name, and update the Deployment's reference. A config change changes the pod template, which triggers a **normal rolling update**, with rollback: the old ConfigMap still exists under its old name
- File mounts plus an app that reloads on change

The hash approach is the safest: config changes go through the same gradual, observable rollout as code changes. Editing a ConfigMap in place changes the config of **every** pod mounting it at once (for files), or of pods at random as they restart (for env vars).

### Stage 5: immutable ConfigMaps

```yaml
immutable: true
```

An immutable ConfigMap can't be edited (only deleted and recreated). The kubelet stops watching it, which reduces API server load on big clusters, and it prevents accidental in-place edits. It pairs naturally with hashed names.

## Advanced problems

### 1. Pod stuck in `CreateContainerConfigError`
The referenced ConfigMap or key doesn't exist (wrong name, other namespace, not created yet). `kubectl describe pod` names it. `optional: true` on the reference lets the pod start without it.

### 2. "I changed the config but nothing happened"
Environment variables are fixed at container start; `subPath` mounts never update. Restart, or use hashed names.

### 3. A config change broke all pods at once
A file-mounted ConfigMap edited in place reached every pod within a minute, with no rollout and no rollback. Version configuration like code: hashed names or a GitOps pipeline.

## Easy to get wrong
- Putting passwords in a ConfigMap: that's what a [[Kubernetes Secret]] is for
- Expecting environment variables to update live
- Using `subPath` and expecting updates
- Editing a shared ConfigMap in place in production
- Forgetting that values are strings (`"8080"`, `"true"`)
- Storing large data: the limit is 1 MiB

## Related
- Sensitive counterpart:: [[Kubernetes Secret]]
- Consumed by:: [[Kubernetes Pod]], [[Kubernetes Deployment]] (rollouts on change)
- Build once, configure at run time:: [[Docker image tags]], [[Docker]]
- In AWS (Amazon Web Services):: [[Systems Manager]] (Parameter Store, AppConfig)
- Overview:: [[Kubernetes]], [[Kubernetes worked example]]
- Area:: [[Containers]]

## Flashcards
#flashcards

What is a ConfigMap for? :: Non-sensitive configuration kept outside the image, as key-value pairs or files
Size limit of a ConfigMap? :: 1 MiB
Two main ways to consume a ConfigMap? :: Environment variables (env/envFrom) and files in a volume
Do environment variables from a ConfigMap update when it changes? :: No, only when the container restarts
Do ConfigMap volume files update? :: Yes, after a delay, except subPath mounts
How do you make a config change trigger a rolling update? :: Put a content hash in the ConfigMap name (Kustomize configMapGenerator) and reference it from the pod template
What does immutable: true do on a ConfigMap? :: Forbids edits and lets the kubelet stop watching it
What error does a missing ConfigMap cause? :: CreateContainerConfigError (unless the reference is optional)
