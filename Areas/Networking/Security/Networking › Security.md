---
type: subtopic
created: 2026-10-09
topic: Networking
tags: [subtopic, networking]
---
# Networking › Security

> What this covers: filtering (ACLs, ingress and egress) and securing traffic: encryption, PKI, TLS, mTLS, workload identity.

Part of [[Networking]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[Ingress and egress]]: traffic into vs out of something, and why it only means something once the boundary is named. Packet direction vs connection direction (stateful vs stateless rules, ephemeral ports), north-south vs east-west, why egress filtering matters, cloud egress fees, and the things named after the words (Kubernetes Ingress, egress gateways)
- [[ACL]]: ordered allow/deny rule lists, stateless vs stateful
- [[Encryption basics]]: symmetric vs asymmetric, Diffie-Hellman, forward secrecy, certificates
- [[Certificates and PKI]]: what's in a certificate, chains, trust stores, public vs private CAs, file formats
- [[TLS]]: protecting one application's connection, handshake, termination at a proxy
- [[mTLS]]: both sides show certificates. Service-to-service authentication, why the client CA must be private
- [[Workload identity (SPIFFE)]]: identities for services without stored secrets

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
