---
type: concept
created: 2026-09-20
topic: Networking
confidence: 2
tags: [networking, protocol]
---
# ICMP

> [!abstract] In one sentence
> **ICMP (Internet Control Message Protocol)** is how network devices send **control messages and error reports** to each other. It's what `ping` and `traceroute` use.

## What it is

ICMP is part of the IP suite and works at **Layer 3 (network layer)**. Unlike TCP and UDP, it doesn't carry application data. It carries information *about* the network: "this host is reachable", "destination unreachable", "TTL expired"…

## A real-world example: `ping`

```bash
ping google.com
```

My computer sends an **ICMP Echo Request**, and if the server answers, I get an **ICMP Echo Reply**:

```
Your Computer                         Google
     │                                  │
     │──── ICMP Echo Request ──────────►│
     │                                  │
     │◄─── ICMP Echo Reply ─────────────│
     │                                  │
     ▼
  Connection works!
```

> [!warning] A failed ping doesn't mean the server is down
> ==Firewalls often block ICMP while allowing HTTP, HTTPS or SSH.==
> On AWS: a new [[EC2]] instance **doesn't answer ping** until its security group allows **ICMP** inbound.

## ICMP vs TCP vs UDP

| Feature | ICMP | TCP | UDP |
|---|---|---|---|
| Main purpose | Network control & error reporting | Reliable data transfer | Fast, connectionless data transfer |
| OSI layer | Layer 3 | Layer 4 | Layer 4 |
| Uses ports? | ❌ No | ✅ Yes | ✅ Yes |
| Connection (handshake)? | ❌ No | ✅ Yes | ❌ No |
| Example | `ping`, `traceroute` | HTTP, SSH, databases | DNS, streaming, VoIP |
| Guaranteed delivery? | ❌ No | ✅ Yes, generally | ❌ No |

## Connects to
- [[EC2]]: security group rule "All ICMP - IPv4" to allow ping
- [[VPC]]: network ACLs can block it too
- [[Networking]]

## Flashcards
#flashcards

What layer is ICMP? :: Layer 3 (network)
Does ICMP use ports? :: No
My EC2 instance doesn't answer ping but HTTP works. Why? :: The security group (or NACL) doesn't allow ICMP inbound
