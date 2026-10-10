---
type: subtopic
created: 2026-10-10
topic: Operating systems
tags: [subtopic, os]
---
# Kernel

> What this covers: where the kernel meets the CPU and the devices: interrupts, exceptions, system calls.

Part of [[Operating systems]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[Interrupts]]: how the outside world reaches a CPU that's busy running a program. Polling vs interrupts, the hardware path (IRQ, I/O APIC, MSI/MSI-X, local APIC, the IDT, `iret`), user mode vs kernel mode, the timer interrupt and preemption (tickless), exceptions (page fault, divide error, invalid opcode, general protection) and how they become SIGSEGV/SIGFPE/SIGILL, system calls as deliberate traps (`int 0x80`, `syscall`, vDSO), DMA, a busy NIC (top/bottom halves, softirqs, ksoftirqd, NAPI, coalescing, RSS multi-queue, IRQ affinity with `/proc/interrupts`, `/proc/softirqs`, `ethtool`), IPIs and TLB shootdowns, NMIs and the lockup watchdog, interrupts vs signals, the classic failures (one CPU at 100 % softirq, ring buffer drops, coalescing trade-offs, interrupt storms, softirq starvation, hard lockups), and ENA queues and steal time on EC2
- Not written yet: *[[System calls]]* (the user/kernel boundary, strace, the vDSO, seccomp)

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
