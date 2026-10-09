---
type: subtopic
created: 2026-10-09
topic: Networking
tags: [subtopic, networking]
---
# Networking › Resilience

> What this covers: surviving slow and failing dependencies: the patterns, the libraries (Hystrix, Resilience4j, Polly, others) and the service mesh.

Part of [[Networking]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[Resilience patterns]]: surviving slow and failing dependencies. Cascading failure, timeouts (and deadlines), retries with backoff, jitter and budgets, circuit breakers, bulkheads and Little's law, fallbacks, rate limiting and load shedding, hedging, the nesting order, why it all lived in application code until about 2018, and what moved to the mesh
- [[Hystrix]]: tutorial for Netflix's Java library (2012, maintenance since 2018): commands, thread vs semaphore isolation, properties, Spring Cloud annotations, the dashboard, and moving off it
- [[Resilience4j]]: tutorial for its Java successor: circuit breaker, retry, time limiter, bulkheads, rate limiter, Spring Boot configuration and annotation order, metrics, traps
- [[Polly]]: tutorial for .NET: v7 policies, v8 resilience pipelines, `AddStandardResilienceHandler`, hedging, chaos testing
- [[Resilience libraries in other languages]]: Go, Python, Node.js, gRPC deadlines and retry policy, Failsafe, Sentinel, adaptive concurrency limits, Finagle, and the cost of a polyglot zoo
- [[Resilience in a service mesh]]: the same patterns as proxy configuration (Istio, Envoy, Linkerd): timeouts, retries and budgets, Envoy "circuit breakers" vs outlier detection, fault injection, what stays in the app, migrating without multiplying retries

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
