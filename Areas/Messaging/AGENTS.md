# Area guide: Messaging

**Index:** `Messaging.md` is the learning path (5 numbered sections, each assumes the ones above) with a one-line summary of every note and the planned notes as italic links. Read it for *what* a note covers; use this file for *where* it is.

**Scope:** vendor-neutral messaging for a systems engineer: queues, pub/sub, event streaming (Kafka), delivery guarantees, event-driven patterns. Cloud specifics live in `Areas/AWS/Integration/` and are linked from here, never mixed in (except a short "In AWS" section at the end of a note).

## Folder map

```
Messaging/
├── Messaging.md                   topic index (the learning path)
├── AMQP.md                        0-9-1 vs 1.0, exchanges/bindings, acks, confirms, durability, DLX
├── MQTT.md                        topics/wildcards, QoS, retained, LWT, sessions, IoT security, IoT Core
├── JMS.md                         Java API (not a protocol), queues/topics, durable subs, selectors, transactions, Amazon MQ
└── Kafka.md                       log, partitions/keys, offsets, consumer groups, replication, exactly-once, compaction, debugging
```

`SQS.md`, `SNS.md`, `EventBridge.md`, `Step Functions.md`, `SQS vs SNS vs EventBridge.md` and `Kafka vs AWS messaging services.md` are listed in this area's index (section 5) but live in `Areas/AWS/Integration/` with `topic: AWS`.

## Where a new note goes

| It's about… | Folder |
|---|---|
| Queue/pub-sub/log shapes, delivery guarantees (section 1) | Area root |
| A protocol or API (AMQP, MQTT, JMS, STOMP) | Area root |
| A broker or streaming platform (RabbitMQ, Kafka, NATS, Pulsar) | Area root, or a folder once 2+ notes share it |
| Architecture patterns (outbox, sagas, CDC) (section 4) | Area root |
| An AWS messaging service (MSK, Kinesis, Step Functions) | `Areas/AWS/Integration/`, `topic: AWS`, listed in section 5 of `Messaging.md` |

The planned notes (roadmap) are the italic `*[[…]]*` links in `Messaging.md`: when writing one, use that exact name so existing links resolve.
