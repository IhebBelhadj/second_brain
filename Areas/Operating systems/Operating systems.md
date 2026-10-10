---
type: topic
created: 2026-10-10
tags: [topic, os]
aliases: [OS, Operating system]
---
# Operating systems

> What this covers: what the kernel does for the processes running on one machine, seen from Linux as a systems engineer meets it: how processes talk and get signalled, how memory is virtualized, how the hardware gets the CPU's attention. Examples are plain processes (small Python and C programs, `strace`, `/proc`), so every mechanism can be watched on any Linux box.

## Sub-topics
Each sub-topic has its own index with the same reading order, for studying one part at a time (and a cleaner graph).
- [[Operating systems › Processes]]: processes and threads, how they talk (IPC, signals) and how they share safely (locks)
- [[Operating systems › Memory]]: virtual memory, the life of a page, the page cache, the OOM killer
- [[Operating systems › Kernel]]: where the kernel meets the CPU and devices: interrupts, system calls
- [[Operating systems › Case studies]]: real software read through the concepts: a web server's processes, PostgreSQL

## How to use this

Read top to bottom. Links in *italics* are notes not written yet (the roadmap).

## 1. Processes and how they talk
- [[Processes and threads]]: a program vs a process and what the kernel keeps for each (task_struct, /proc/<pid>/status), the process tree from PID 1 (pstree), fork then exec and why they're two steps (redirections in between, strace of a shell, vfork/posix_spawn), exit and wait, process states (R, S, D, T, Z) and why Linux load average counts D, voluntary vs involuntary context switches and their cost, threads as clone() tasks sharing an address space (clone flags, TIDs, ps -eLf, /proc/<pid>/task, top -H), what threads share vs own, the GIL, processes vs threads trade-offs, server concurrency models (process per connection, pre-forked pool, thread per connection, thread pool, event loop, hybrids) and C10k, task limits (pid_max, threads-max, ulimit -u, pids.max), and the failures (fork bombs and EAGAIN, high load with idle CPUs, thousands of threads, fork in a threaded program, defunct processes, too many connections in a process-per-connection server)
- [[Inter-process communication]]: how processes on one machine talk, at the process level. Separate memory even after fork (copy-on-write), file descriptors, files (rename, flock, inotify), pipes (pipe + fork, closing unused ends, end-of-file, PIPE_BUF, how the shell builds a pipeline) and FIFOs, signals (handlers, SIGTERM vs SIGKILL, zombies), Unix domain sockets (server and client, permissions, peer credentials, fd passing, stale socket files), shared memory (the lost-update race and locks), and what's left across machines
- [[Signals]]: how the kernel interrupts a process with a number. The signal table and the five default actions, pending and blocked sets and delivery on return to user mode (read from `/proc/<pid>/status`), sending and permissions (`kill`, `kill -0`, negative PGID), handlers with `sigaction` and Python's `signal`, async-signal-safety (why `printf`/`malloc` in a handler deadlocks; flag, self-pipe, `signalfd`), masks and critical sections, signals and threads, `EINTR` and `SA_RESTART`, standard vs real-time signals, `SIGCHLD`/`waitpid`, zombies, orphans and subreapers, process groups, sessions and job control (Ctrl-C/Ctrl-Z, `fg`/`bg`, `SIGHUP`, `nohup`, `setsid`), signals from CPU exceptions and 128 + n exit codes, `SIGALRM`, core dumps, the stop sequences of systemd, Docker and Kubernetes, PID 1 in containers (shell-form `CMD`, tini), and the traps (Ctrl-C ignored, orphaned workers, zombie pile-up, handler deadlock, `SIGPIPE` killing servers, `EINTR`, `docker stop` taking 10 s)
- [[Locks and synchronization]]: four workers, one counter, opened up. Race conditions and critical sections, why disabling interrupts can't work on multicore, atomic instructions (fetch-and-add, test-and-set, CAS), a spinlock built by hand and when spinning hurts, memory ordering (acquire/release, why volatile isn't enough), futexes and mutexes (no system call when uncontended, traced with strace), locks between processes (process-shared mutexes, semaphores, flock/fcntl and lslocks), reader-writer locks, condition variables and lost wake-ups, the layers of locks in a database-like program, deadlocks (four conditions, lock ordering, wait-for graphs), livelock, starvation and priority inversion, contention (cache-line bouncing, false sharing, partitioned and lock-free designs), robust mutexes and restarting everything when a holder dies, and the failures (lost updates, deadlocked services, spinning CPUs, stale lock files)
- Not written yet: *[[CPU scheduling]]* (run queues, priorities, nice, load average)

## 2. Memory
- [[Virtual memory]]: the mechanism as a chain of reasons. Two processes, one address, two values; why translate at all (relocation, isolation, fragmentation, RAM size); why fixed-size pages (not bytes, not whole programs); how an address splits into page number and offset, and why 4 KiB; why 48 bits and 128 TiB; why the page table is a sparse 4-level tree (a flat one would be 256 GiB; what each level's entry covers, where 48 bits come from); why the TLB exists and why it must stay tiny (TLB reach); huge pages as bigger entries higher in the tree; switching processes (CR3, PCID, shootdowns); page faults (minor, major, invalid). Then what it enables (demand paging, sharing and copy-on-write, the page cache, swap and thrashing, overcommit and the OOM killer) and how to read it on a machine (/proc/pid/maps, ASLR, VSZ/RSS/PSS/USS, free vs available, cgroup limits and exit 137), with the failures (OOM-killed database, container OOM with free host RAM, false alarms, thrashing, TLB misses on big data sets, RSS that never shrinks, fork failing under strict overcommit)
- [[Memory pages]]: one page through its life, using a small storage engine with its own 8 KiB pages. Page size (getconf, 4/16/64 KiB, huge pages), what a page table entry holds (present, write, user, NX, and the accessed/dirty bits the CPU sets), struct page, zones, NUMA nodes and the buddy allocator, anonymous vs file-backed and clean vs dirty (what reclaim can do with each, read from /proc/meminfo), reading into the page cache, dirty pages and writeback (flusher threads, dirty_background_ratio/dirty_ratio, fsync), reclaim (active/inactive LRU lists, kswapd vs direct reclaim, swappiness, sar -B), application page vs kernel page vs filesystem block vs sector (torn pages, full page images, doublewrite), double buffering, O_DIRECT and fadvise/madvise hints, shared memory pages (Shmem isn't droppable cache, page tables multiplied by many processes), explicit huge pages vs THP, mlock, the zero page and KSM, reading smaps, and the failures (dirty_ratio stalls, fsync storms, a backup evicting hot data, swapping with "free" cache, torn pages, gigabytes of page tables, drop_caches as a "fix")

## 3. The kernel and the hardware
- [[Interrupts]]: how the outside world reaches a CPU that's busy running a program. Polling vs interrupts, the hardware path (IRQ, I/O APIC, MSI/MSI-X, local APIC, the IDT, `iret`), user mode vs kernel mode, the timer interrupt and preemption (tickless), exceptions (page fault, divide error, invalid opcode, general protection) and how they become SIGSEGV/SIGFPE/SIGILL, system calls as deliberate traps (`int 0x80`, `syscall`, vDSO), DMA, a busy NIC (top/bottom halves, softirqs, ksoftirqd, NAPI, coalescing, RSS multi-queue, IRQ affinity with `/proc/interrupts`, `/proc/softirqs`, `ethtool`), IPIs and TLB shootdowns, NMIs and the lockup watchdog, interrupts vs signals, the classic failures (one CPU at 100 % softirq, ring buffer drops, coalescing trade-offs, interrupt storms, softirq starvation, hard lockups), and ENA queues and steal time on EC2
- Not written yet: *[[System calls]]* (the user/kernel boundary, strace, the vDSO, seccomp)

## 4. Case studies
- [[Inter-process communication on a web server]]: the same mechanisms on one real server: export handoff with rename, log tailing, pipes when debugging, SIGHUP reloads and SIGTERM deploys, nginx → gunicorn over a Unix socket, PostgreSQL's shared memory, what changes on many machines, and the failures (502 permission denied, stale sockets, cut requests, too many open files, /dev/shm in containers)
- [[PostgreSQL architecture]]: the capstone, PostgreSQL read through every concept in this area, observed with OS tools. The postmaster as supervisor and a forked backend per connection (process titles, helper processes, why processes not threads, connection costs and pooling), one shared region mapped into every process (shared_buffers, WAL buffers, lock tables, anonymous mmap + tiny System V segment, DSM in /dev/shm, the RSS illusion, page tables and huge_pages), 8 KiB pages over 4 KiB kernel pages (a read's path, clock sweep and rings, double buffering, who writes dirty pages, torn pages and full_page_writes), durability (WAL first, LSNs, commit = fdatasync, checkpoints, recovery, fsyncgate), three layers of locks (spinlocks, LWLocks, lock manager, row locks in xmax, deadlocks, MVCC, wait events), signals and IPC (SIGHUP reload, smart/fast/immediate shutdown, cancel vs terminate, latches, logger pipe, Unix socket peer auth), one crash resets everyone (kill -9, the OOM killer, oom_score_adj, overcommit), memory per backend and sizing (work_mem multiplication, memory contexts, cgroups), 10 failure modes, and RDS/Aurora

## Related areas
- [[Networking]]: where processes stop sharing a kernel: [[Sockets]], [[Network interfaces]] (namespaces, loopback)
- [[Storage]]: disks, filesystems and mounting ([[Partitions and filesystems]])
- [[Containers]]: namespaces and cgroups used for isolation (*[[Container internals]]*), PID 1 and signals in [[Docker]]

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE topic = this.file.name AND confidence
SORT confidence ASC
```
