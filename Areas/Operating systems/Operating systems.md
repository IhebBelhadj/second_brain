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
- [[Operating systems › Processes]]: processes and how they talk: IPC, signals
- [[Operating systems › Memory]]: virtual memory, paging, the page cache, the OOM killer
- [[Operating systems › Kernel]]: where the kernel meets the CPU and devices: interrupts, system calls

## How to use this

Read top to bottom. Links in *italics* are notes not written yet (the roadmap).

## 1. Processes and how they talk
- [[Inter-process communication]]: how processes on one machine talk, at the process level. Separate memory even after fork (copy-on-write), file descriptors, files (rename, flock, inotify), pipes (pipe + fork, closing unused ends, end-of-file, PIPE_BUF, how the shell builds a pipeline) and FIFOs, signals (handlers, SIGTERM vs SIGKILL, zombies), Unix domain sockets (server and client, permissions, peer credentials, fd passing, stale socket files), shared memory (the lost-update race and locks), and what's left across machines
    - [[Inter-process communication on a web server]]: the same mechanisms on one real server: export handoff with rename, log tailing, pipes when debugging, SIGHUP reloads and SIGTERM deploys, nginx → gunicorn over a Unix socket, PostgreSQL's shared memory, what changes on many machines, and the failures (502 permission denied, stale sockets, cut requests, too many open files, /dev/shm in containers)
- [[Signals]]: how the kernel interrupts a process with a number. The signal table and the five default actions, pending and blocked sets and delivery on return to user mode (read from `/proc/<pid>/status`), sending and permissions (`kill`, `kill -0`, negative PGID), handlers with `sigaction` and Python's `signal`, async-signal-safety (why `printf`/`malloc` in a handler deadlocks; flag, self-pipe, `signalfd`), masks and critical sections, signals and threads, `EINTR` and `SA_RESTART`, standard vs real-time signals, `SIGCHLD`/`waitpid`, zombies, orphans and subreapers, process groups, sessions and job control (Ctrl-C/Ctrl-Z, `fg`/`bg`, `SIGHUP`, `nohup`, `setsid`), signals from CPU exceptions and 128 + n exit codes, `SIGALRM`, core dumps, the stop sequences of systemd, Docker and Kubernetes, PID 1 in containers (shell-form `CMD`, tini), and the traps (Ctrl-C ignored, orphaned workers, zombie pile-up, handler deadlock, `SIGPIPE` killing servers, `EINTR`, `docker stop` taking 10 s)
- Not written yet: *[[Processes and threads]]* (fork/exec, process states, threads vs processes) · *[[CPU scheduling]]* (run queues, priorities, nice, load average)

## 2. Memory
- [[Virtual memory]]: two processes, one address, two values. Why physical addressing failed (relocation, isolation, fragmentation, RAM size), per-process address spaces, pages and frames, multi-level page tables, the MMU and TLB (context switches, shootdowns), demand paging and page faults (minor, major, invalid → SIGSEGV) measured with perf, sharing (libraries, copy-on-write after fork, mmap), the page cache and free vs available, the process layout in /proc/pid/maps and ASLR, VSZ vs RSS vs PSS vs USS, overcommit and the OOM killer, swap and thrashing, huge pages and THP, cgroup limits in containers (exit 137, OOMKilled, JVM sizing), and the failures (OOM-killed database, container OOM with free host RAM, page-cache false alarms, thrashing, THP latency, leak vs fragmentation, fork failing under strict overcommit)

## 3. The kernel and the hardware
- [[Interrupts]]: how the outside world reaches a CPU that's busy running a program. Polling vs interrupts, the hardware path (IRQ, I/O APIC, MSI/MSI-X, local APIC, the IDT, `iret`), user mode vs kernel mode, the timer interrupt and preemption (tickless), exceptions (page fault, divide error, invalid opcode, general protection) and how they become SIGSEGV/SIGFPE/SIGILL, system calls as deliberate traps (`int 0x80`, `syscall`, vDSO), DMA, a busy NIC (top/bottom halves, softirqs, ksoftirqd, NAPI, coalescing, RSS multi-queue, IRQ affinity with `/proc/interrupts`, `/proc/softirqs`, `ethtool`), IPIs and TLB shootdowns, NMIs and the lockup watchdog, interrupts vs signals, the classic failures (one CPU at 100 % softirq, ring buffer drops, coalescing trade-offs, interrupt storms, softirq starvation, hard lockups), and ENA queues and steal time on EC2
- Not written yet: *[[System calls]]* (the user/kernel boundary, strace, the vDSO, seccomp)

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
