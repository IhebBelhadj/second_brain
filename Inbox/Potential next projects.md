### Distributed web crawler and search index
Crawl at scale with per-host politeness (robots.txt, rate limits), a partitioned URL frontier, near-duplicate detection (SimHash), and Bloom-filter deduplication.

Hard parts: assigning hosts to workers by consistent hashing so politeness is enforced locally, spider traps, re-crawl scheduling by change frequency, and frontier persistence that survives restarts.
Java angle: high-concurrency I/O (virtual threads or Netty), HTML parsing, and compact frontier structures.
Kubernetes role: worker pool autoscaling and a headless Service for peer discovery. Apache StormCrawler and Nutch are good references.


### Real-time dispatch engine (Uber-style matching)
Drivers stream locations, riders request rides, and the system matches them in real time.

Hard parts: geospatial sharding with H3 cells, handling entities that move across shard boundaries, batched matching (optimizing across many requests rather than greedy nearest-first), and ETA estimation.
Java angle: an in-memory spatial index per shard, plus a simulator generating thousands of moving agents.
Kubernetes role: shards as a StatefulSet with live rebalancing. A map visualization of the simulation makes a great demo.