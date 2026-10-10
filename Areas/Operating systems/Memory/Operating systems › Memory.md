---
type: subtopic
created: 2026-10-10
topic: Operating systems
tags: [subtopic, os]
---
# Operating systems › Memory

> What this covers: how the kernel gives each process its own memory: virtual address spaces, paging, the page cache, overcommit and the OOM killer, memory limits in containers.

Part of [[Operating systems]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[Virtual memory]]: two processes, one address, two values. Why physical addressing failed (relocation, isolation, fragmentation, RAM size), per-process address spaces, pages and frames, multi-level page tables, the MMU and TLB (context switches, shootdowns), demand paging and page faults (minor, major, invalid → SIGSEGV) measured with perf, sharing (libraries, copy-on-write after fork, mmap), the page cache and free vs available, the process layout in /proc/pid/maps and ASLR, VSZ vs RSS vs PSS vs USS, overcommit and the OOM killer, swap and thrashing, huge pages and THP, cgroup limits in containers (exit 137, OOMKilled, JVM sizing), and the failures (OOM-killed database, container OOM with free host RAM, page-cache false alarms, thrashing, THP latency, leak vs fragmentation, fork failing under strict overcommit)
- [[Memory pages]]: one page through its life, using a small storage engine with its own 8 KiB pages. Page size (getconf, 4/16/64 KiB, huge pages), what a page table entry holds (present, write, user, NX, and the accessed/dirty bits the CPU sets), struct page, zones, NUMA nodes and the buddy allocator, anonymous vs file-backed and clean vs dirty (what reclaim can do with each, read from /proc/meminfo), reading into the page cache, dirty pages and writeback (flusher threads, dirty_background_ratio/dirty_ratio, fsync), reclaim (active/inactive LRU lists, kswapd vs direct reclaim, swappiness, sar -B), application page vs kernel page vs filesystem block vs sector (torn pages, full page images, doublewrite), double buffering, O_DIRECT and fadvise/madvise hints, shared memory pages (Shmem isn't droppable cache, page tables multiplied by many processes), explicit huge pages vs THP, mlock, the zero page and KSM, reading smaps, and the failures (dirty_ratio stalls, fsync storms, a backup evicting hot data, swapping with "free" cache, torn pages, gigabytes of page tables, drop_caches as a "fix")

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
