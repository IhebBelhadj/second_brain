---
type: subtopic
created: 2026-10-09
topic: Storage
tags: [subtopic, storage]
---
# Storage › Network storage

> What this covers: sharing storage over the network: how it works, NFS and SMB.

Part of [[Storage]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[NFS and SMB]]: sharing a filesystem with many machines. NFS on Linux (exports, versions, UID/GID trust, root_squash) vs SMB on Windows (users, ACLs, Samba), **which OS can mount which** (Windows' NFS client is v3 only), stale handles, hard vs soft mounts, locking, small-file slowness
- [[How network file sharing works]]: under the hood. RPC and COMPOUND, the first file handle at mount, what a file handle is (and why it goes stale), a read and a write followed across both page caches, UNSTABLE writes and COMMIT, close-to-open consistency, leases, locks, grace periods, delegations and callbacks through NAT, network failures, the same shape in SMB, watching it with mountstats and Wireshark

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
