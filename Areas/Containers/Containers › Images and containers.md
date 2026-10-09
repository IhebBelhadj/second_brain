---
type: subtopic
created: 2026-10-09
topic: Containers
tags: [subtopic, containers]
---
# Containers › Images and containers

> What this covers: building, tagging and running images on one host: Docker, tags, Compose.

Part of [[Containers]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[Docker]]: from "it works on my machine" to an image. Layers and the build cache, instruction order, secrets that stay in layers, multi-stage builds, BuildKit cache and secret mounts, PID 1 and signals, ports and bind addresses, volumes, the build-once deployment flow, multi-arch builds, and the production traps (published ports bypassing the firewall, Docker Hub limits behind NAT, full disks, exit 137)
- [[Docker image tags]]: learning tags hands-on (untagged images, `-t`, several tags on one image, rebuilding moves a tag, full names with the registry, pushing, digests vs tags, pulling on other machines), choosing a tagging scheme (commit, release, floating, environment tags), build once and promote, deploying by digest, and what goes wrong (`latest`, races, moving base images, fake rollbacks, multi-arch, retention)
- [[Docker Compose]]: from four `docker run` commands to one `compose.yaml`. Project names, the project network and service-name DNS, `depends_on` vs readiness (health checks), variables, override files and profiles, the `.env` trap, `compose watch`, running it on a server, and why it isn't an orchestrator (port conflicts when scaling, "lost" volumes, external networks, secrets)

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
