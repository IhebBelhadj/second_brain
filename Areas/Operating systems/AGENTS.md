# Area guide: Operating systems

**Index:** `Operating systems.md` is the learning path with a one-line summary of every note and the planned notes as italic links. Read it for *what* a note covers; use this file for *where* it is.

**Scope:** what the kernel does for processes on one machine, as a systems engineer meets it on Linux: processes and how they talk (IPC, signals), memory (virtual memory, paging, the OOM killer), and the kernel's contact with the hardware (interrupts, system calls). Examples are plain processes (small Python/C programs, `strace`, `/proc`), not a particular application. Networking between machines is the Networking area; disks and filesystems are the Storage area; container isolation (namespaces, cgroups) is the Containers area.

## Folder map

```
Operating systems/
├── Operating systems.md           topic index (the learning path)
├── Processes/                     processes and how they talk
│   ├── Operating systems › Processes.md   sub-topic index
│   ├── Processes and threads.md   program vs process, fork/exec, states, context switches, threads, concurrency models, limits
│   ├── Inter-process communication.md     process level: fork/copy-on-write, fds, files, pipes, FIFOs, signals, Unix sockets, shared memory
│   ├── Signals.md                 kernel delivery, default actions, handlers, masks, process groups/terminal, PID 1, stop sequences
│   └── Locks and synchronization.md   races, atomics, spinlocks, futex/mutex, cross-process locks, RW locks, deadlocks, contention
├── Memory/
│   ├── Operating systems › Memory.md      sub-topic index
│   ├── Virtual memory.md          pages, page tables, MMU/TLB, page faults, COW, page cache, RSS/PSS, overcommit/OOM, swap, THP, cgroup limits
│   └── Memory pages.md            PTE bits, anonymous vs file, dirty/writeback/fsync, reclaim/LRU, app page vs block (torn pages), huge pages, mlock
├── Kernel/
│   ├── Operating systems › Kernel.md      sub-topic index
│   └── Interrupts.md              hardware IRQs, kernel mode, top/bottom halves, timer and preemption, exceptions, syscalls, NIC path, affinity
└── Case studies/                  real software read through the concepts above
    ├── Operating systems › Case studies.md   sub-topic index
    ├── Inter-process communication on a web server.md   nginx/gunicorn/PostgreSQL/cron on one host, failures
    └── PostgreSQL architecture.md processes, shared memory and pages, locks, signals and IPC inside PostgreSQL
```

## Sub-topics

Every note in this area has `subtopic: <index name>` in its frontmatter, and is linked from that sub-topic index (`type: subtopic`, tag `subtopic`). The area index `Operating systems.md` links every sub-topic index in its "Sub-topics" section.

| Sub-topic index | Lives in | Covers |
|---|---|---|
| `Operating systems › Processes.md` | `Processes/` | processes and threads, how they talk (IPC, signals), how they share safely (locks) |
| `Operating systems › Memory.md` | `Memory/` | virtual memory, the life of a page, the page cache, the OOM killer |
| `Operating systems › Kernel.md` | `Kernel/` | where the kernel meets the CPU and devices: interrupts, system calls |
| `Operating systems › Case studies.md` | `Case studies/` | real software read through the concepts: a web server's processes, PostgreSQL |

A new note gets the `subtopic` of the folder it goes in, and a line in that sub-topic index as well as in `Operating systems.md`.

## Where a new note goes

| It's about… | Folder |
|---|---|
| Processes, threads, scheduling, IPC, signals | `Processes/` |
| Memory: paging, allocation, caches, OOM | `Memory/` |
| Kernel/hardware boundary: interrupts, system calls, boot, drivers | `Kernel/` |
| A real program explained with these concepts (a database, a web server, a runtime) | `Case studies/` |
| Network sockets and protocols | The Networking area ([[Sockets]] stays there) |
| Disks, filesystems, mounting | The Storage area |
| Namespaces and cgroups as container isolation | The Containers area |

The planned notes (roadmap) are the italic `*[[…]]*` links in `Operating systems.md`: when writing one, use that exact name so existing links resolve.
