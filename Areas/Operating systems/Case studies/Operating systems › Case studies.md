---
type: subtopic
created: 2026-10-10
topic: Operating systems
tags: [subtopic, os]
---
# Operating systems › Case studies

> What this covers: real software read through the concepts of this area: the processes on one web server, and PostgreSQL's processes, shared memory, pages, locks and signals.

Part of [[Operating systems]]. Same reading order as the full index; each note assumes the ones above it (and the rest of the area).

## Notes, in reading order
- [[Inter-process communication on a web server]]: the same mechanisms on one real server: export handoff with rename, log tailing, pipes when debugging, SIGHUP reloads and SIGTERM deploys, nginx → gunicorn over a Unix socket, PostgreSQL's shared memory, what changes on many machines, and the failures (502 permission denied, stale sockets, cut requests, too many open files, /dev/shm in containers)
- [[PostgreSQL architecture]]: the capstone, PostgreSQL read through every concept in this area, observed with OS tools. The postmaster as supervisor and a forked backend per connection (process titles, helper processes, why processes not threads, connection costs and pooling), one shared region mapped into every process (shared_buffers, WAL buffers, lock tables, anonymous mmap + tiny System V segment, DSM in /dev/shm, the RSS illusion, page tables and huge_pages), 8 KiB pages over 4 KiB kernel pages (a read's path, clock sweep and rings, double buffering, who writes dirty pages, torn pages and full_page_writes), durability (WAL first, LSNs, commit = fdatasync, checkpoints, recovery, fsyncgate), three layers of locks (spinlocks, LWLocks, lock manager, row locks in xmax, deadlocks, MVCC, wait events), signals and IPC (SIGHUP reload, smart/fast/immediate shutdown, cancel vs terminate, latches, logger pipe, Unix socket peer auth), one crash resets everyone (kill -9, the OOM killer, oom_score_adj, overcommit), memory per backend and sizing (work_mem multiplication, memory contexts, cgroups), 10 failure modes, and RDS/Aurora

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
