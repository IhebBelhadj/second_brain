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
- [[Virtual memory]]: the mechanism as a chain of reasons. Two processes, one address, two values; why translate at all (relocation, isolation, fragmentation, RAM size); why fixed-size pages (not bytes, not whole programs); how an address splits into page number and offset, and why 4 KiB; why 48 bits and 128 TiB; why the page table is a 4-level tree (a flat one would be 256 GiB); why the TLB exists and why it must stay tiny (TLB reach, huge pages, context switches, shootdowns); page faults (minor, major, invalid). Then what it enables (demand paging, sharing and copy-on-write, the page cache, swap and thrashing, overcommit and the OOM killer) and how to read it on a machine (/proc/pid/maps, ASLR, VSZ/RSS/PSS/USS, free vs available, cgroup limits and exit 137), with the failures (OOM-killed database, container OOM with free host RAM, false alarms, thrashing, TLB misses on big data sets, RSS that never shrinks, fork failing under strict overcommit)
- [[Memory pages]]: one page through its life, using a small storage engine with its own 8 KiB pages. Page size (getconf, 4/16/64 KiB, huge pages), what a page table entry holds (present, write, user, NX, and the accessed/dirty bits the CPU sets), struct page, zones, NUMA nodes and the buddy allocator, anonymous vs file-backed and clean vs dirty (what reclaim can do with each, read from /proc/meminfo), reading into the page cache, dirty pages and writeback (flusher threads, dirty_background_ratio/dirty_ratio, fsync), reclaim (active/inactive LRU lists, kswapd vs direct reclaim, swappiness, sar -B), application page vs kernel page vs filesystem block vs sector (torn pages, full page images, doublewrite), double buffering, O_DIRECT and fadvise/madvise hints, shared memory pages (Shmem isn't droppable cache, page tables multiplied by many processes), explicit huge pages vs THP, mlock, the zero page and KSM, reading smaps, and the failures (dirty_ratio stalls, fsync storms, a backup evicting hot data, swapping with "free" cache, torn pages, gigabytes of page tables, drop_caches as a "fix")

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
