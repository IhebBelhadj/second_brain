---
type: subtopic
created: 2026-10-09
topic: AWS
tags: [subtopic, aws]
---
# AWS integration

> What this covers: services talking without waiting for each other: SQS, SNS, EventBridge, Step Functions.

Part of [[AWS]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[SQS]]: queues. Consumers pull and delete, visibility timeout and duplicates, dead-letter queues, standard vs FIFO (message groups), scaling workers on queue depth, Lambda batches
- [[SNS]]: pub/sub topics. One publish → every subscriber, fan-out to one SQS queue per consumer, filter policies, the envelope and raw delivery
- [[EventBridge]]: event buses and rules. Reacting to AWS's own events, routing my events by content, Scheduler, cross-account buses, archive and replay, Pipes
- [[SQS vs SNS vs EventBridge]]: which one (and which combination), plus when the answer is Kinesis, Amazon MQ or Step Functions instead
- [[Step Functions]]: serverless workflows. State types, Standard vs Express, the three ways a task waits (.sync, callback), Retry/Catch and sagas, Distributed Map over S3, a catalogue of architectures, and how it differs from Airflow
- [[Kafka vs AWS messaging services]]: Kafka (a replayable log) next to MSK, Kinesis, SQS, SNS and EventBridge, the exam keywords for each, and a design that combines them

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
