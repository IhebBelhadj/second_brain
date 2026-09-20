---
type: note
created: 2026-09-20
topic:
tags: []
---
## What is ICMP 

**ICMP (Internet Control Message Protocol)** is a network protocol used by devices to **send control messages and report network errors**. It's part of the IP protocol suite and operates at **Layer 3 (Network Layer)** of the OSI model. Unlike TCP and UDP, ICMP is not used to transport application data. It's primarily used to communicate information about network connectivity and problems. --- ## 1. A real-world example: `ping` The most common use of ICMP is the `ping` command. When you run: ```bash ping google.com``` 


Your computer sends an **ICMP Echo Request** to Google's server.
If the server responds, you receive an **ICMP Echo Reply**.

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

> **Important:** A failed ping does not necessarily mean that a server is down. Firewalls can block ICMP while allowing HTTP, HTTPS, or SSH traffic.

| Feature                   | ICMP                                | TCP                             | UDP                                    |
| ------------------------- | ----------------------------------- | ------------------------------- | -------------------------------------- |
| Main purpose              | Network control and error reporting | Reliable data transmission      | Fast, connectionless data transmission |
| OSI layer                 | Layer 3                             | Layer 4                         | Layer 4                                |
| Uses ports?               | ❌ No                                | ✅ Yes                           | ✅ Yes                                  |
| Establishes a connection? | ❌ No                                | ✅ Yes (handshake)               | ❌ No                                   |
| Example                   | `ping`                              | HTTP, SSH, database connections | DNS, streaming, VoIP                   |
| Guarantees delivery?      | ❌ No                                | ✅ Yes, generally                | ❌ No                                   |
