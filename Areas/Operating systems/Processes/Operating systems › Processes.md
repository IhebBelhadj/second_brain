---
type: subtopic
created: 2026-10-10
topic: Operating systems
tags: [subtopic, os]
---
# Operating systems › Processes

> What this covers: processes and how they talk to each other: inter-process communication (files, pipes, signals, Unix sockets, shared memory) and signals in depth.

Part of [[Operating systems]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[Inter-process communication]]: how processes on one machine talk, at the process level. Separate memory even after fork (copy-on-write), file descriptors, files (rename, flock, inotify), pipes (pipe + fork, closing unused ends, end-of-file, PIPE_BUF, how the shell builds a pipeline) and FIFOs, signals (handlers, SIGTERM vs SIGKILL, zombies), Unix domain sockets (server and client, permissions, peer credentials, fd passing, stale socket files), shared memory (the lost-update race and locks), and what's left across machines
    - [[Inter-process communication on a web server]]: the same mechanisms on one real server: export handoff with rename, log tailing, pipes when debugging, SIGHUP reloads and SIGTERM deploys, nginx → gunicorn over a Unix socket, PostgreSQL's shared memory, what changes on many machines, and the failures (502 permission denied, stale sockets, cut requests, too many open files, /dev/shm in containers)
- [[Signals]]: how the kernel interrupts a process with a number. The signal table and the five default actions, pending and blocked sets and delivery on return to user mode (read from `/proc/<pid>/status`), sending and permissions (`kill`, `kill -0`, negative PGID), handlers with `sigaction` and Python's `signal`, async-signal-safety (why `printf`/`malloc` in a handler deadlocks; flag, self-pipe, `signalfd`), masks and critical sections, signals and threads, `EINTR` and `SA_RESTART`, standard vs real-time signals, `SIGCHLD`/`waitpid`, zombies, orphans and subreapers, process groups, sessions and job control (Ctrl-C/Ctrl-Z, `fg`/`bg`, `SIGHUP`, `nohup`, `setsid`), signals from CPU exceptions and 128 + n exit codes, `SIGALRM`, core dumps, the stop sequences of systemd, Docker and Kubernetes, PID 1 in containers (shell-form `CMD`, tini), and the traps (Ctrl-C ignored, orphaned workers, zombie pile-up, handler deadlock, `SIGPIPE` killing servers, `EINTR`, `docker stop` taking 10 s)
- Not written yet: *[[Processes and threads]]* (fork/exec, process states, threads vs processes) · *[[CPU scheduling]]* (run queues, priorities, nice, load average)

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
