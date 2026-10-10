---
type: subtopic
created: 2026-10-10
topic: Operating systems
tags: [subtopic, os]
---
# Processes

> What this covers: processes and how they talk to each other: inter-process communication (files, pipes, signals, Unix sockets, shared memory) and signals in depth.

Part of [[Operating systems]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[Processes and threads]]: a program vs a process and what the kernel keeps for each (task_struct, /proc/<pid>/status), the process tree from PID 1 (pstree), fork then exec and why they're two steps (redirections in between, strace of a shell, vfork/posix_spawn), exit and wait, process states (R, S, D, T, Z) and why Linux load average counts D, voluntary vs involuntary context switches and their cost, threads as clone() tasks sharing an address space (clone flags, TIDs, ps -eLf, /proc/<pid>/task, top -H), what threads share vs own, the GIL, processes vs threads trade-offs, server concurrency models (process per connection, pre-forked pool, thread per connection, thread pool, event loop, hybrids) and C10k, task limits (pid_max, threads-max, ulimit -u, pids.max), and the failures (fork bombs and EAGAIN, high load with idle CPUs, thousands of threads, fork in a threaded program, defunct processes, too many connections in a process-per-connection server)
- [[Inter-process communication]]: how processes on one machine talk, at the process level. Separate memory even after fork (copy-on-write), file descriptors, files (rename, flock, inotify), pipes (pipe + fork, closing unused ends, end-of-file, PIPE_BUF, how the shell builds a pipeline) and FIFOs, signals (handlers, SIGTERM vs SIGKILL, zombies), Unix domain sockets (server and client, permissions, peer credentials, fd passing, stale socket files), shared memory (the lost-update race and locks), and what's left across machines
- [[Signals]]: how the kernel interrupts a process with a number. The signal table and the five default actions, pending and blocked sets and delivery on return to user mode (read from `/proc/<pid>/status`), sending and permissions (`kill`, `kill -0`, negative PGID), handlers with `sigaction` and Python's `signal`, async-signal-safety (why `printf`/`malloc` in a handler deadlocks; flag, self-pipe, `signalfd`), masks and critical sections, signals and threads, `EINTR` and `SA_RESTART`, standard vs real-time signals, `SIGCHLD`/`waitpid`, zombies, orphans and subreapers, process groups, sessions and job control (Ctrl-C/Ctrl-Z, `fg`/`bg`, `SIGHUP`, `nohup`, `setsid`), signals from CPU exceptions and 128 + n exit codes, `SIGALRM`, core dumps, the stop sequences of systemd, Docker and Kubernetes, PID 1 in containers (shell-form `CMD`, tini), and the traps (Ctrl-C ignored, orphaned workers, zombie pile-up, handler deadlock, `SIGPIPE` killing servers, `EINTR`, `docker stop` taking 10 s)
- [[Locks and synchronization]]: four workers, one counter, opened up. Race conditions and critical sections, why disabling interrupts can't work on multicore, atomic instructions (fetch-and-add, test-and-set, CAS), a spinlock built by hand and when spinning hurts, memory ordering (acquire/release, why volatile isn't enough), futexes and mutexes (no system call when uncontended, traced with strace), locks between processes (process-shared mutexes, semaphores, flock/fcntl and lslocks), reader-writer locks, condition variables and lost wake-ups, the layers of locks in a database-like program, deadlocks (four conditions, lock ordering, wait-for graphs), livelock, starvation and priority inversion, contention (cache-line bouncing, false sharing, partitioned and lock-free designs), robust mutexes and restarting everything when a holder dies, and the failures (lost updates, deadlocked services, spinning CPUs, stale lock files)
- Not written yet: *[[CPU scheduling]]* (run queues, priorities, nice, load average)

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
